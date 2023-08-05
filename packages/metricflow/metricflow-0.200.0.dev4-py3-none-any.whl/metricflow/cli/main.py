from __future__ import annotations

import datetime as dt
import logging
import os
import pathlib
import signal
import sys
import textwrap
import time
from importlib.metadata import version as pkg_version
from typing import Callable, List, Optional

import click
import jinja2
import pandas as pd
from dbt_semantic_interfaces.implementations.semantic_manifest import PydanticSemanticManifest
from dbt_semantic_interfaces.validations.semantic_manifest_validator import SemanticManifestValidator
from dbt_semantic_interfaces.validations.validator_helpers import SemanticManifestValidationResults
from halo import Halo
from packaging.version import parse
from update_checker import UpdateChecker

import metricflow.cli.custom_click_types as click_custom
from metricflow.cli import PACKAGE_NAME
from metricflow.cli.cli_context import CLIContext
from metricflow.cli.constants import DEFAULT_RESULT_DECIMAL_PLACES, MAX_LIST_OBJECT_ELEMENTS
from metricflow.cli.tutorial import create_sample_data, gen_sample_model_configs, remove_sample_tables
from metricflow.cli.utils import (
    MF_BIGQUERY_KEYS,
    MF_CONFIG_KEYS,
    MF_DATABRICKS_KEYS,
    MF_POSTGRESQL_KEYS,
    MF_REDSHIFT_KEYS,
    MF_SNOWFLAKE_KEYS,
    exception_handler,
    generate_duckdb_demo_keys,
    get_data_warehouse_config_link,
    query_options,
    start_end_time_options,
)
from metricflow.configuration.config_builder import YamlTemplateBuilder
from metricflow.dag.dag_visualization import display_dag_as_svg
from metricflow.dataflow.dataflow_plan_to_text import dataflow_plan_as_text
from metricflow.engine.metricflow_engine import MetricFlowExplainResult, MetricFlowQueryRequest, MetricFlowQueryResult
from metricflow.engine.utils import model_build_result_from_config
from metricflow.model.data_warehouse_model_validator import DataWarehouseModelValidator
from metricflow.sql_clients.common_client import SqlDialect
from metricflow.telemetry.models import TelemetryLevel
from metricflow.telemetry.reporter import TelemetryReporter, log_call

logger = logging.getLogger(__name__)

pass_config = click.make_pass_decorator(CLIContext, ensure=True)
_telemetry_reporter = TelemetryReporter(report_levels_higher_or_equal_to=TelemetryLevel.USAGE)
_telemetry_reporter.add_python_log_handler()
_telemetry_reporter.add_rudderstack_handler()


@click.group()
@click.option("-v", "--verbose", is_flag=True)
@pass_config
@log_call(module_name=__name__, telemetry_reporter=_telemetry_reporter)
def cli(cfg: CLIContext, verbose: bool) -> None:  # noqa: D
    cfg.verbose = verbose

    checker = UpdateChecker()
    result = checker.check(PACKAGE_NAME, pkg_version(PACKAGE_NAME))
    # result is None when an update was not found or a failure occurred
    if result:
        click.secho(
            "‼️ Warning: A new version of the MetricFlow CLI is available.",
            bold=True,
            fg="red",
        )

        click.echo(
            f"💡 Please update to version {result.available_version}, released {result.release_date} by running:\n"
            f"\t$ pip install --upgrade {PACKAGE_NAME}\n",
        )

    # Cancel queries submitted to the DW if the user precess CTRL + c / process is terminated.
    # Note: docs unclear on the type for the 'frame' argument.
    def exit_signal_handler(signal_type: int, frame) -> None:  # type: ignore
        if signal_type == signal.SIGINT:
            click.echo("Got SIGINT")
        elif signal_type == signal.SIGTERM:
            click.echo("Got SIGTERM")
        else:
            # Shouldn't happen since this should ony be registered for SIGINT / SIGTERM.
            click.echo(f"Got unhandled signal {signal_type}")
            return

        try:
            if cfg.sql_client.sql_engine_attributes.cancel_submitted_queries_supported:
                logger.info("Cancelling submitted queries")
                cfg.sql_client.cancel_submitted_queries()
                cfg.sql_client.close()
        finally:
            sys.exit(-1)

    signal.signal(signal.SIGINT, exit_signal_handler)
    signal.signal(signal.SIGTERM, exit_signal_handler)


@cli.command()
@click.option("--restart", is_flag=True, help="Wipe the config file and start over")
@pass_config
@log_call(module_name=__name__, telemetry_reporter=_telemetry_reporter)
def setup(cfg: CLIContext, restart: bool) -> None:
    """Setup MetricFlow."""
    click.echo(
        textwrap.dedent(
            """\
            🎉 Welcome to MetricFlow! 🎉
            """
        )
    )

    path = pathlib.Path(cfg.config.file_path)
    abs_path = path.absolute()
    to_create = not path.exists() or restart

    # Seed the config template to the config file
    if to_create:
        dialect_map = {
            SqlDialect.SNOWFLAKE.value: MF_SNOWFLAKE_KEYS,
            SqlDialect.BIGQUERY.value: MF_BIGQUERY_KEYS,
            SqlDialect.REDSHIFT.value: MF_REDSHIFT_KEYS,
            SqlDialect.POSTGRESQL.value: MF_POSTGRESQL_KEYS,
            SqlDialect.DUCKDB.value: generate_duckdb_demo_keys(config_dir=cfg.config.dir_path),
            SqlDialect.DATABRICKS.value: MF_DATABRICKS_KEYS,
        }

        click.echo("Please enter your data warehouse dialect.")
        click.echo("Use 'duckdb' for a standalone demo.")
        click.echo("")
        dialect = click.prompt(
            "Dialect",
            type=click.Choice(sorted([x for x in dialect_map.keys()])),
            show_choices=True,
        )

        # If there is a collision, prefer to use the key in the dialect.
        config_keys = list(dialect_map[dialect])
        for mf_config_key in MF_CONFIG_KEYS:
            if not any(x.key == mf_config_key.key for x in config_keys):
                config_keys.append(mf_config_key)

        with open(abs_path, "w") as file:
            YamlTemplateBuilder.write_yaml(config_keys, file)

    template_description = (
        f"A template config file has been created in {abs_path}.\n"
        if to_create
        else f"A template config file already exists in {abs_path}, so it was left alone.\n"
    )
    click.echo(
        textwrap.dedent(
            f"""\
            💻 {template_description}
            If you are new to MetricFlow, we recommend you to run through our tutorial with `mf tutorial`\n
            Next steps:
              1. Review and fill out relevant fields.
              2. Run `mf health-checks` to validate the data warehouse connection.
              3. Run `mf validate-configs` to validate the model configurations.
            """
        )
    )


@cli.command()
@click.option("-m", "--msg", is_flag=True, help="Output the final steps dialogue")
@click.option("--skip-dw", is_flag=True, help="Skip the data warehouse health checks")
@click.option("--drop-tables", is_flag=True, help="Drop all the dummy tables created via tutorial")
@pass_config
@click.pass_context
@log_call(module_name=__name__, telemetry_reporter=_telemetry_reporter)
def tutorial(ctx: click.core.Context, cfg: CLIContext, msg: bool, skip_dw: bool, drop_tables: bool) -> None:
    """Run user through a tutorial."""
    # This text is also located in the projects top-level README.md
    help_msg = textwrap.dedent(
        """\
        🤓 Please run the following steps,

            1.  In '{$HOME}/.metricflow/config.yml', `model_path` should be '{$HOME}/.metricflow/sample_models'.
            2.  Try validating your data model: `mf validate-configs`
            3.  Check out your metrics: `mf list-metrics`
            4.  Check out dimensions for your metric `mf list-dimensions --metric-names transactions`
            5.  Query your first metric: `mf query --metrics transactions --dimensions metric_time --order metric_time`
            6.  Show the SQL MetricFlow generates:
                `mf query --metrics transactions --dimensions metric_time --order metric_time --explain`
            7.  Visualize the plan:
                `mf query --metrics transactions --dimensions metric_time --order metric_time --explain --display-plans`
                * This only works if you have graphviz installed - see README.
            8.  Add another dimension:
                `mf query --metrics transactions --dimensions metric_time,customer__country --order metric_time`
            9.  Add a coarser time granularity:
                `mf query --metrics transactions --dimensions metric_time__week --order metric_time__week`
            10. Try a more complicated query:
                `mf query \\
                  --metrics transactions,transaction_usd_na,transaction_usd_na_l7d --dimensions metric_time,is_large \\
                  --order metric_time --start-time 2022-03-20 --end-time 2022-04-01`
                * You can also add `--explain` or `--display-plans`.
            11. For more ways to interact with the sample models, go to
                ‘https://docs.transform.co/docs/metricflow/metricflow-tutorial’.
            12. Once you’re done, run `mf tutorial --skip-dw --drop-tables` to drop the sample tables.
        """
    )

    if msg:
        click.echo(help_msg)
        exit()

    # Check if the MetricFlow configuration file exists
    path = pathlib.Path(cfg.config.file_path)
    if not path.absolute().exists():
        click.echo("💡 Please run `mf setup` to get your configs set up before going through the tutorial.")
        exit()

    # Validate that the data warehouse connection is successful
    if not skip_dw:
        ctx.invoke(health_checks)
        click.confirm("❓ Are the health-checks all passing? Please fix them before continuing", abort=True)
        click.echo("💡 For future reference, you can continue with the tutorial by adding `--skip-dw`\n")

    if drop_tables:
        spinner = Halo(text="Dropping tables...", spinner="dots")
        spinner.start()
        remove_sample_tables(sql_client=cfg.sql_client, system_schema=cfg.mf_system_schema)
        spinner.succeed("Tables dropped")
        exit()

    # Seed sample data into data warehouse
    spinner = Halo(text=f"🤖 Generating sample data into schema {cfg.mf_system_schema}...", spinner="dots")
    spinner.start()
    created = create_sample_data(sql_client=cfg.sql_client, system_schema=cfg.mf_system_schema)
    if not created:
        spinner.warn("🙊 Skipped creating sample tables since they already exist.")
    else:
        spinner.succeed("📀 Sample tables have been successfully created into your data warehouse.")

    # Seed sample model file
    model_path = os.path.join(cfg.config.dir_path, "sample_models")
    pathlib.Path(model_path).mkdir(parents=True, exist_ok=True)
    click.echo(f"🤖 Attempting to generate model configs to your local filesystem in '{str(model_path)}'.")
    spinner = Halo(text="Dropping tables...", spinner="dots")
    spinner.start()
    gen_sample_model_configs(dir_path=str(model_path), system_schema=cfg.mf_system_schema)
    spinner.succeed(f"📜 Model configs has been generated into '{model_path}'")

    click.echo(help_msg)
    click.echo("💡 Run `mf tutorial --msg` to see this message again without executing everything else")
    exit()


@cli.command()
@query_options
@click.option(
    "--csv",
    type=click.File("wb"),
    required=False,
    help="Provide filepath for dataframe output to csv",
)
@click.option(
    "--explain",
    is_flag=True,
    required=False,
    default=False,
    help="In the query output, show the query that was executed against the data warehouse",
)
@click.option(
    "--show-dataflow-plan",
    is_flag=True,
    required=False,
    default=False,
    help="Display dataflow plan in explain output",
)
@click.option(
    "--display-plans",
    is_flag=True,
    required=False,
    help="Display plans (e.g. metric dataflow) in the browser",
)
@click.option(
    "--decimals",
    required=False,
    default=2,
    help="Choose the number of decimal places to round for the numerical values",
)
@click.option(
    "--show-sql-descriptions",
    is_flag=True,
    default=False,
    help="Shows inline descriptions of nodes in displayed SQL",
)
@pass_config
@exception_handler
@log_call(module_name=__name__, telemetry_reporter=_telemetry_reporter)
def query(
    cfg: CLIContext,
    metrics: List[str],
    group_bys: List[str] = [],
    where: Optional[str] = None,
    start_time: Optional[dt.datetime] = None,
    end_time: Optional[dt.datetime] = None,
    order: Optional[List[str]] = None,
    limit: Optional[int] = None,
    csv: Optional[click.utils.LazyFile] = None,
    explain: bool = False,
    show_dataflow_plan: bool = False,
    display_plans: bool = False,
    decimals: int = DEFAULT_RESULT_DECIMAL_PLACES,
    show_sql_descriptions: bool = False,
) -> None:
    """Create a new query with MetricFlow and assembles a MetricFlowQueryResult."""
    start = time.time()
    spinner = Halo(text="Initiating query…", spinner="dots")
    spinner.start()

    mf_request = MetricFlowQueryRequest.create_with_random_request_id(
        metric_names=metrics,
        group_by_names=group_bys,
        limit=limit,
        time_constraint_start=start_time,
        time_constraint_end=end_time,
        where_constraint=where,
        order_by_names=order,
    )

    explain_result: Optional[MetricFlowExplainResult] = None
    query_result: Optional[MetricFlowQueryResult] = None

    if explain:
        explain_result = cfg.mf.explain(mf_request=mf_request)
    else:
        query_result = cfg.mf.query(mf_request=mf_request)

    spinner.succeed(f"Success 🦄 - query completed after {time.time() - start:.2f} seconds")

    if explain:
        assert explain_result
        sql = (
            explain_result.rendered_sql_without_descriptions.sql_query
            if not show_sql_descriptions
            else explain_result.rendered_sql.sql_query
        )
        if show_dataflow_plan:
            click.echo("🔎 Generated Dataflow Plan + SQL (remove --explain to see data):")
            click.echo(
                textwrap.indent(
                    jinja2.Template(
                        textwrap.dedent(
                            """\
                            Metric Dataflow Plan:
                                {{ plan_text | indent(4) }}
                            """
                        ),
                        undefined=jinja2.StrictUndefined,
                    ).render(plan_text=dataflow_plan_as_text(explain_result.dataflow_plan)),
                    prefix="-- ",
                )
            )
            click.echo("")
        else:
            click.echo(
                "🔎 SQL (remove --explain to see data or add --show-dataflow-plan to see the generated dataflow plan):"
            )
        click.echo(sql)
        if display_plans:
            svg_path = display_dag_as_svg(explain_result.dataflow_plan, cfg.config.dir_path)
            click.echo("")
            click.echo(f"Plan SVG saved to: {svg_path}")
        exit()

    assert query_result
    df = query_result.result_df
    # Show the data if returned successfully
    if df is not None:
        if df.empty:
            click.echo("🕳 Successful MQL query returned an empty result set.")
        elif csv is not None:
            # csv is a LazyFile that is file-like that works in this case.
            df.to_csv(csv, index=False)  # type: ignore
            click.echo(f"🖨 Successfully written query output to {csv.name}")
        else:
            # NOTE: remove `to_string` if no pandas dependency is < 1.1.0
            if parse(pd.__version__) >= parse("1.1.0"):
                click.echo(df.to_markdown(index=False, floatfmt=f".{decimals}f"))
            else:
                click.echo(df.to_string(index=False, float_format=lambda x: format(x, f".{decimals}f")))

        if display_plans:
            svg_path = display_dag_as_svg(query_result.dataflow_plan, cfg.config.dir_path)
            click.echo(f"Plan SVG saved to: {svg_path}")


@cli.group()
@pass_config
@log_call(module_name=__name__, telemetry_reporter=_telemetry_reporter)
def list(cfg: CLIContext) -> None:  # noqa: D
    """Retrieve metadata values about metrics/dimensions/entities/dimension values."""


@list.command()
@click.option("--search", required=False, type=str, help="Filter available metrics by this search term")
@click.option(
    "--show-all-dimensions", is_flag=True, default=False, help="Show all dimensions associated with a metric."
)
@pass_config
@exception_handler
@log_call(module_name=__name__, telemetry_reporter=_telemetry_reporter)
def metrics(cfg: CLIContext, show_all_dimensions: bool = False, search: Optional[str] = None) -> None:
    """List the metrics with their available dimensions.

    Automatically truncates long lists of dimensions, pass --show-all-dims to see all.
    """
    spinner = Halo(text="🔍 Looking for all available metrics...", spinner="dots")
    spinner.start()

    metrics = cfg.mf.list_metrics()

    if not metrics:
        spinner.fail("List of metrics unavailable.")

    filter_msg = ""
    if search is not None:
        num_metrics = len(metrics)
        metrics = [m for m in metrics if search.lower() in m.name.lower()]
        filter_msg = f" matching `{search}`, of a total of {num_metrics} available"

    spinner.succeed(f"🌱 We've found {len(metrics)} metrics{filter_msg}.")
    click.echo('The list below shows metrics in the format of "metric_name: list of available dimensions"')
    num_dims_to_show = MAX_LIST_OBJECT_ELEMENTS
    for m in metrics:
        # sort dimensions by whether they're local first(if / then global else local) then the dim name
        dimensions = sorted(map(lambda d: d.name, filter(lambda d: "/" not in d.name, m.dimensions))) + sorted(
            map(lambda d: d.name, filter(lambda d: "/" in d.name, m.dimensions))
        )
        if show_all_dimensions:
            num_dims_to_show = len(dimensions)
        click.echo(
            f"• {click.style(m.name, bold=True, fg='green')}: {', '.join(dimensions[:num_dims_to_show])}"
            + (f" and {len(dimensions) - num_dims_to_show} more" if len(dimensions) > num_dims_to_show else "")
        )


@list.command()
@click.option(
    "--metrics",
    type=click_custom.SequenceParamType(min_length=1),
    default="",
    help="List dimensions by given metrics (intersection). Ex. --metrics bookings,messages",
)
@pass_config
@exception_handler
@log_call(module_name=__name__, telemetry_reporter=_telemetry_reporter)
def dimensions(cfg: CLIContext, metrics: List[str]) -> None:
    """List all unique dimensions."""
    spinner = Halo(
        text="🔍 Looking for all available dimensions...",
        spinner="dots",
    )
    spinner.start()

    dimensions = cfg.mf.simple_dimensions_for_metrics(metrics)
    if not dimensions:
        spinner.fail("List of dimensions unavailable.")

    spinner.succeed(f"🌱 We've found {len(dimensions)} common dimensions for metrics {metrics}.")
    for d in dimensions:
        click.echo(f"• {click.style(d.name, bold=True, fg='green')}")


@cli.command()
@pass_config
@exception_handler
@log_call(module_name=__name__, telemetry_reporter=_telemetry_reporter)
def health_checks(cfg: CLIContext) -> None:
    """Performs a health check against the DW provided in the configs."""
    click.echo(f"For specifics on the health-checks, please visit {get_data_warehouse_config_link(cfg.config)}")
    spinner = Halo(
        text="🏥 Running health checks against your data warehouse... (This should not take longer than 30s for a successful connection)",
        spinner="dots",
    )
    spinner.start()
    res = cfg.run_health_checks()
    spinner.succeed("Health checks completed.")
    for test in res:
        test_res = res[test]
        if test_res["status"] != "SUCCESS":
            click.echo(f"• ❌ {click.style(test, bold=True, fg=('red'))}:  Failed with - {test_res['error_message']}.")
        else:
            click.echo(f"• ✅ {click.style(test, bold=True, fg=('green'))}: Success!")


@list.command()
@click.option("--dimension", required=True, type=str, help="Dimension to query values from")
@click.option("--metric", required=True, type=str, help="Metric that is associated with the dimension")
@start_end_time_options
@pass_config
@exception_handler
@log_call(module_name=__name__, telemetry_reporter=_telemetry_reporter)
def dimension_values(
    cfg: CLIContext,
    metric: str,
    dimension: str,
    start_time: Optional[dt.datetime] = None,
    end_time: Optional[dt.datetime] = None,
) -> None:
    """List all dimension values with the corresponding metric."""
    spinner = Halo(
        text=f"🔍 Retrieving dimension values for dimension '{dimension}' of metric '{metric}'...",
        spinner="dots",
    )
    spinner.start()

    dim_vals: Optional[List[str]] = None

    try:
        dim_vals = cfg.mf.get_dimension_values(
            metric_name=metric,
            get_group_by_values=dimension,
            time_constraint_start=start_time,
            time_constraint_end=end_time,
        )
    except Exception as e:
        spinner.fail()
        click.echo(
            textwrap.dedent(
                f"""\
                ❌ Failed to query dimension values for dimension {dimension} of metric {metric}.
                    ERROR: {str(e)}
                """
            )
        )
        exit(1)

    assert dim_vals
    spinner.succeed(f"🌱 We've found {len(dim_vals)} dimension values for dimension {dimension} of metric {metric}.")
    for dim_val in dim_vals:
        click.echo(f"• {click.style(dim_val, bold=True, fg='green')}")


def _print_issues(
    issues: SemanticManifestValidationResults, show_non_blocking: bool = False, verbose: bool = False
) -> None:  # noqa: D
    for issue in issues.errors:
        print(f"• {issue.as_cli_formatted_str(verbose=verbose)}")
    if show_non_blocking:
        for issue in issues.future_errors:
            print(f"• {issue.as_cli_formatted_str(verbose=verbose)}")
        for issue in issues.warnings:
            print(f"• {issue.as_cli_formatted_str(verbose=verbose)}")


def _run_dw_validations(
    validation_func: Callable[[PydanticSemanticManifest, Optional[int]], SemanticManifestValidationResults],
    validation_type: str,
    model: PydanticSemanticManifest,
    timeout: Optional[int],
) -> SemanticManifestValidationResults:
    """Helper handles the calling of data warehouse issue generating functions."""
    spinner = Halo(text=f"Validating {validation_type} against data warehouse...", spinner="dots")
    spinner.start()

    results = validation_func(model, timeout)
    if not results.has_blocking_issues:
        spinner.succeed(f"🎉 Successfully validated {validation_type} against data warehouse ({results.summary()})")
    else:
        spinner.fail(
            f"Breaking issues found when validating {validation_type} against data warehouse ({results.summary()})"
        )
    return results


def _data_warehouse_validations_runner(
    dw_validator: DataWarehouseModelValidator, model: PydanticSemanticManifest, timeout: Optional[int]
) -> SemanticManifestValidationResults:
    """Helper which calls the individual data warehouse validations to run and prints collected issues."""
    semantic_model_results = _run_dw_validations(
        dw_validator.validate_semantic_models, model=model, validation_type="semantic models", timeout=timeout
    )
    dimension_results = _run_dw_validations(
        dw_validator.validate_dimensions, model=model, validation_type="dimensions", timeout=timeout
    )
    entity_results = _run_dw_validations(
        dw_validator.validate_entities, model=model, validation_type="entities", timeout=timeout
    )
    measure_results = _run_dw_validations(
        dw_validator.validate_measures, model=model, validation_type="measures", timeout=timeout
    )
    metric_results = _run_dw_validations(
        dw_validator.validate_metrics, model=model, validation_type="metrics", timeout=timeout
    )

    return SemanticManifestValidationResults.merge(
        [semantic_model_results, dimension_results, entity_results, measure_results, metric_results]
    )


@cli.command()
@click.option(
    "--dw-timeout", required=False, type=int, help="Optional timeout for data warehouse validation steps. Default None."
)
@click.option(
    "--skip-dw",
    is_flag=True,
    default=False,
    help="If specified, skips the data warehouse validations",
)
@click.option("--show-all", is_flag=True, default=False, help="If specified, prints warnings and future-errors")
@click.option(
    "--verbose-issues", is_flag=True, default=False, help="If specified, prints any extra details issues might have"
)
@click.option(
    "--semantic-validation-workers",
    required=False,
    type=int,
    default=1,
    help="Optional. Uses the number of workers specified to run the semantic validations. Should only be used for exceptionally large configs",
)
@pass_config
@exception_handler
@log_call(module_name=__name__, telemetry_reporter=_telemetry_reporter)
def validate_configs(
    cfg: CLIContext,
    dw_timeout: Optional[int] = None,
    skip_dw: bool = False,
    show_all: bool = False,
    verbose_issues: bool = False,
    semantic_validation_workers: int = 1,
) -> None:
    """Perform validations against the defined model configurations."""
    cfg.verbose = True

    if not show_all:
        print("(To see warnings and future-errors, run again with flag `--show-all`)")

    # Parsing Validation
    parsing_spinner = Halo(text="Building model from configs", spinner="dots")
    parsing_spinner.start()

    parsing_result = model_build_result_from_config(handler=cfg.config, raise_issues_as_exceptions=False)

    if not parsing_result.issues.has_blocking_issues:
        parsing_spinner.succeed(f"🎉 Successfully built model from configs ({parsing_result.issues.summary()})")
    else:
        parsing_spinner.fail(
            f"Breaking issues found when building model from configs ({parsing_result.issues.summary()})"
        )
        _print_issues(parsing_result.issues, show_non_blocking=show_all, verbose=verbose_issues)
        return

    user_model = parsing_result.semantic_manifest

    # Semantic validation
    semantic_spinner = Halo(text="Validating semantics of built model", spinner="dots")
    semantic_spinner.start()
    model_issues = SemanticManifestValidator[PydanticSemanticManifest](
        max_workers=semantic_validation_workers
    ).validate_semantic_manifest(user_model)

    if not model_issues.has_blocking_issues:
        semantic_spinner.succeed(f"🎉 Successfully validated the semantics of built model ({model_issues.summary()})")
    else:
        semantic_spinner.fail(
            f"Breaking issues found when checking semantics of built model ({model_issues.summary()})"
        )
        _print_issues(model_issues, show_non_blocking=show_all, verbose=verbose_issues)
        return

    dw_results = SemanticManifestValidationResults()
    if not skip_dw:
        dw_validator = DataWarehouseModelValidator(sql_client=cfg.sql_client, system_schema=cfg.mf_system_schema)
        dw_results = _data_warehouse_validations_runner(dw_validator=dw_validator, model=user_model, timeout=dw_timeout)

    merged_results = SemanticManifestValidationResults.merge([parsing_result.issues, model_issues, dw_results])
    _print_issues(merged_results, show_non_blocking=show_all, verbose=verbose_issues)


if __name__ == "__main__":
    cli()
