-- Compute Metrics via Expressions
SELECT
  metric_time
  , non_referred + (instant * 1.0 / bookings) AS instant_plus_non_referred_bookings_pct
FROM (
  -- Combine Metrics
  SELECT
    COALESCE(subq_34.metric_time, subq_39.metric_time, subq_44.metric_time) AS metric_time
    , subq_34.non_referred AS non_referred
    , subq_39.instant AS instant
    , subq_44.bookings AS bookings
  FROM (
    -- Compute Metrics via Expressions
    SELECT
      metric_time
      , (bookings - ref_bookings) * 1.0 / bookings AS non_referred
    FROM (
      -- Combine Metrics
      SELECT
        COALESCE(subq_27.metric_time, subq_32.metric_time) AS metric_time
        , subq_27.ref_bookings AS ref_bookings
        , subq_32.bookings AS bookings
      FROM (
        -- Aggregate Measures
        -- Compute Metrics via Expressions
        SELECT
          metric_time
          , SUM(referred_bookings) AS ref_bookings
        FROM (
          -- Read Elements From Semantic Model 'bookings_source'
          -- Metric Time Dimension 'ds'
          -- Pass Only Elements:
          --   ['referred_bookings', 'metric_time']
          SELECT
            ds AS metric_time
            , CASE WHEN referrer_id IS NOT NULL THEN 1 ELSE 0 END AS referred_bookings
          FROM ***************************.fct_bookings bookings_source_src_10001
        ) subq_25
        GROUP BY
          metric_time
      ) subq_27
      INNER JOIN (
        -- Aggregate Measures
        -- Compute Metrics via Expressions
        SELECT
          metric_time
          , SUM(bookings) AS bookings
        FROM (
          -- Read Elements From Semantic Model 'bookings_source'
          -- Metric Time Dimension 'ds'
          -- Pass Only Elements:
          --   ['bookings', 'metric_time']
          SELECT
            ds AS metric_time
            , 1 AS bookings
          FROM ***************************.fct_bookings bookings_source_src_10001
        ) subq_30
        GROUP BY
          metric_time
      ) subq_32
      ON
        (
          subq_27.metric_time = subq_32.metric_time
        ) OR (
          (subq_27.metric_time IS NULL) AND (subq_32.metric_time IS NULL)
        )
    ) subq_33
  ) subq_34
  INNER JOIN (
    -- Aggregate Measures
    -- Compute Metrics via Expressions
    SELECT
      metric_time
      , SUM(instant_bookings) AS instant
    FROM (
      -- Read Elements From Semantic Model 'bookings_source'
      -- Metric Time Dimension 'ds'
      -- Pass Only Elements:
      --   ['instant_bookings', 'metric_time']
      SELECT
        ds AS metric_time
        , CASE WHEN is_instant THEN 1 ELSE 0 END AS instant_bookings
      FROM ***************************.fct_bookings bookings_source_src_10001
    ) subq_37
    GROUP BY
      metric_time
  ) subq_39
  ON
    (
      subq_34.metric_time = subq_39.metric_time
    ) OR (
      (subq_34.metric_time IS NULL) AND (subq_39.metric_time IS NULL)
    )
  INNER JOIN (
    -- Aggregate Measures
    -- Compute Metrics via Expressions
    SELECT
      metric_time
      , SUM(bookings) AS bookings
    FROM (
      -- Read Elements From Semantic Model 'bookings_source'
      -- Metric Time Dimension 'ds'
      -- Pass Only Elements:
      --   ['bookings', 'metric_time']
      SELECT
        ds AS metric_time
        , 1 AS bookings
      FROM ***************************.fct_bookings bookings_source_src_10001
    ) subq_42
    GROUP BY
      metric_time
  ) subq_44
  ON
    (
      subq_34.metric_time = subq_44.metric_time
    ) OR (
      (subq_34.metric_time IS NULL) AND (subq_44.metric_time IS NULL)
    )
) subq_45
