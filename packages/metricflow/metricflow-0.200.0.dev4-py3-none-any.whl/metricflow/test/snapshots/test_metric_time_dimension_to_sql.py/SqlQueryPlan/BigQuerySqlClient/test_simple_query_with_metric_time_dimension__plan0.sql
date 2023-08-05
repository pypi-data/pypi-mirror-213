-- Combine Metrics
SELECT
  COALESCE(subq_4.metric_time, subq_9.metric_time) AS metric_time
  , MAX(subq_4.bookings) AS bookings
  , MAX(subq_9.booking_payments) AS booking_payments
FROM (
  -- Compute Metrics via Expressions
  SELECT
    subq_3.metric_time
    , subq_3.bookings
  FROM (
    -- Aggregate Measures
    SELECT
      subq_2.metric_time
      , SUM(subq_2.bookings) AS bookings
    FROM (
      -- Pass Only Elements:
      --   ['bookings', 'metric_time']
      SELECT
        subq_1.metric_time
        , subq_1.bookings
      FROM (
        -- Metric Time Dimension 'ds'
        SELECT
          subq_0.ds
          , subq_0.ds__week
          , subq_0.ds__month
          , subq_0.ds__quarter
          , subq_0.ds__year
          , subq_0.ds_partitioned
          , subq_0.ds_partitioned__week
          , subq_0.ds_partitioned__month
          , subq_0.ds_partitioned__quarter
          , subq_0.ds_partitioned__year
          , subq_0.booking_paid_at
          , subq_0.booking_paid_at__week
          , subq_0.booking_paid_at__month
          , subq_0.booking_paid_at__quarter
          , subq_0.booking_paid_at__year
          , subq_0.create_a_cycle_in_the_join_graph__ds
          , subq_0.create_a_cycle_in_the_join_graph__ds__week
          , subq_0.create_a_cycle_in_the_join_graph__ds__month
          , subq_0.create_a_cycle_in_the_join_graph__ds__quarter
          , subq_0.create_a_cycle_in_the_join_graph__ds__year
          , subq_0.create_a_cycle_in_the_join_graph__ds_partitioned
          , subq_0.create_a_cycle_in_the_join_graph__ds_partitioned__week
          , subq_0.create_a_cycle_in_the_join_graph__ds_partitioned__month
          , subq_0.create_a_cycle_in_the_join_graph__ds_partitioned__quarter
          , subq_0.create_a_cycle_in_the_join_graph__ds_partitioned__year
          , subq_0.create_a_cycle_in_the_join_graph__booking_paid_at
          , subq_0.create_a_cycle_in_the_join_graph__booking_paid_at__week
          , subq_0.create_a_cycle_in_the_join_graph__booking_paid_at__month
          , subq_0.create_a_cycle_in_the_join_graph__booking_paid_at__quarter
          , subq_0.create_a_cycle_in_the_join_graph__booking_paid_at__year
          , subq_0.ds AS metric_time
          , subq_0.ds__week AS metric_time__week
          , subq_0.ds__month AS metric_time__month
          , subq_0.ds__quarter AS metric_time__quarter
          , subq_0.ds__year AS metric_time__year
          , subq_0.listing
          , subq_0.guest
          , subq_0.host
          , subq_0.create_a_cycle_in_the_join_graph
          , subq_0.create_a_cycle_in_the_join_graph__listing
          , subq_0.create_a_cycle_in_the_join_graph__guest
          , subq_0.create_a_cycle_in_the_join_graph__host
          , subq_0.is_instant
          , subq_0.create_a_cycle_in_the_join_graph__is_instant
          , subq_0.bookings
          , subq_0.instant_bookings
          , subq_0.booking_value
          , subq_0.max_booking_value
          , subq_0.min_booking_value
          , subq_0.bookers
          , subq_0.average_booking_value
          , subq_0.referred_bookings
          , subq_0.median_booking_value
          , subq_0.booking_value_p99
          , subq_0.discrete_booking_value_p99
          , subq_0.approximate_continuous_booking_value_p99
          , subq_0.approximate_discrete_booking_value_p99
        FROM (
          -- Read Elements From Semantic Model 'bookings_source'
          SELECT
            1 AS bookings
            , CASE WHEN is_instant THEN 1 ELSE 0 END AS instant_bookings
            , bookings_source_src_10001.booking_value
            , bookings_source_src_10001.booking_value AS max_booking_value
            , bookings_source_src_10001.booking_value AS min_booking_value
            , bookings_source_src_10001.guest_id AS bookers
            , bookings_source_src_10001.booking_value AS average_booking_value
            , bookings_source_src_10001.booking_value AS booking_payments
            , CASE WHEN referrer_id IS NOT NULL THEN 1 ELSE 0 END AS referred_bookings
            , bookings_source_src_10001.booking_value AS median_booking_value
            , bookings_source_src_10001.booking_value AS booking_value_p99
            , bookings_source_src_10001.booking_value AS discrete_booking_value_p99
            , bookings_source_src_10001.booking_value AS approximate_continuous_booking_value_p99
            , bookings_source_src_10001.booking_value AS approximate_discrete_booking_value_p99
            , bookings_source_src_10001.is_instant
            , bookings_source_src_10001.ds
            , DATE_TRUNC(bookings_source_src_10001.ds, isoweek) AS ds__week
            , DATE_TRUNC(bookings_source_src_10001.ds, month) AS ds__month
            , DATE_TRUNC(bookings_source_src_10001.ds, quarter) AS ds__quarter
            , DATE_TRUNC(bookings_source_src_10001.ds, isoyear) AS ds__year
            , bookings_source_src_10001.ds_partitioned
            , DATE_TRUNC(bookings_source_src_10001.ds_partitioned, isoweek) AS ds_partitioned__week
            , DATE_TRUNC(bookings_source_src_10001.ds_partitioned, month) AS ds_partitioned__month
            , DATE_TRUNC(bookings_source_src_10001.ds_partitioned, quarter) AS ds_partitioned__quarter
            , DATE_TRUNC(bookings_source_src_10001.ds_partitioned, isoyear) AS ds_partitioned__year
            , bookings_source_src_10001.booking_paid_at
            , DATE_TRUNC(bookings_source_src_10001.booking_paid_at, isoweek) AS booking_paid_at__week
            , DATE_TRUNC(bookings_source_src_10001.booking_paid_at, month) AS booking_paid_at__month
            , DATE_TRUNC(bookings_source_src_10001.booking_paid_at, quarter) AS booking_paid_at__quarter
            , DATE_TRUNC(bookings_source_src_10001.booking_paid_at, isoyear) AS booking_paid_at__year
            , bookings_source_src_10001.is_instant AS create_a_cycle_in_the_join_graph__is_instant
            , bookings_source_src_10001.ds AS create_a_cycle_in_the_join_graph__ds
            , DATE_TRUNC(bookings_source_src_10001.ds, isoweek) AS create_a_cycle_in_the_join_graph__ds__week
            , DATE_TRUNC(bookings_source_src_10001.ds, month) AS create_a_cycle_in_the_join_graph__ds__month
            , DATE_TRUNC(bookings_source_src_10001.ds, quarter) AS create_a_cycle_in_the_join_graph__ds__quarter
            , DATE_TRUNC(bookings_source_src_10001.ds, isoyear) AS create_a_cycle_in_the_join_graph__ds__year
            , bookings_source_src_10001.ds_partitioned AS create_a_cycle_in_the_join_graph__ds_partitioned
            , DATE_TRUNC(bookings_source_src_10001.ds_partitioned, isoweek) AS create_a_cycle_in_the_join_graph__ds_partitioned__week
            , DATE_TRUNC(bookings_source_src_10001.ds_partitioned, month) AS create_a_cycle_in_the_join_graph__ds_partitioned__month
            , DATE_TRUNC(bookings_source_src_10001.ds_partitioned, quarter) AS create_a_cycle_in_the_join_graph__ds_partitioned__quarter
            , DATE_TRUNC(bookings_source_src_10001.ds_partitioned, isoyear) AS create_a_cycle_in_the_join_graph__ds_partitioned__year
            , bookings_source_src_10001.booking_paid_at AS create_a_cycle_in_the_join_graph__booking_paid_at
            , DATE_TRUNC(bookings_source_src_10001.booking_paid_at, isoweek) AS create_a_cycle_in_the_join_graph__booking_paid_at__week
            , DATE_TRUNC(bookings_source_src_10001.booking_paid_at, month) AS create_a_cycle_in_the_join_graph__booking_paid_at__month
            , DATE_TRUNC(bookings_source_src_10001.booking_paid_at, quarter) AS create_a_cycle_in_the_join_graph__booking_paid_at__quarter
            , DATE_TRUNC(bookings_source_src_10001.booking_paid_at, isoyear) AS create_a_cycle_in_the_join_graph__booking_paid_at__year
            , bookings_source_src_10001.listing_id AS listing
            , bookings_source_src_10001.guest_id AS guest
            , bookings_source_src_10001.host_id AS host
            , bookings_source_src_10001.guest_id AS create_a_cycle_in_the_join_graph
            , bookings_source_src_10001.listing_id AS create_a_cycle_in_the_join_graph__listing
            , bookings_source_src_10001.guest_id AS create_a_cycle_in_the_join_graph__guest
            , bookings_source_src_10001.host_id AS create_a_cycle_in_the_join_graph__host
          FROM ***************************.fct_bookings bookings_source_src_10001
        ) subq_0
      ) subq_1
    ) subq_2
    GROUP BY
      metric_time
  ) subq_3
) subq_4
FULL OUTER JOIN (
  -- Compute Metrics via Expressions
  SELECT
    subq_8.metric_time
    , subq_8.booking_payments
  FROM (
    -- Aggregate Measures
    SELECT
      subq_7.metric_time
      , SUM(subq_7.booking_payments) AS booking_payments
    FROM (
      -- Pass Only Elements:
      --   ['booking_payments', 'metric_time']
      SELECT
        subq_6.metric_time
        , subq_6.booking_payments
      FROM (
        -- Metric Time Dimension 'booking_paid_at'
        SELECT
          subq_5.ds
          , subq_5.ds__week
          , subq_5.ds__month
          , subq_5.ds__quarter
          , subq_5.ds__year
          , subq_5.ds_partitioned
          , subq_5.ds_partitioned__week
          , subq_5.ds_partitioned__month
          , subq_5.ds_partitioned__quarter
          , subq_5.ds_partitioned__year
          , subq_5.booking_paid_at
          , subq_5.booking_paid_at__week
          , subq_5.booking_paid_at__month
          , subq_5.booking_paid_at__quarter
          , subq_5.booking_paid_at__year
          , subq_5.create_a_cycle_in_the_join_graph__ds
          , subq_5.create_a_cycle_in_the_join_graph__ds__week
          , subq_5.create_a_cycle_in_the_join_graph__ds__month
          , subq_5.create_a_cycle_in_the_join_graph__ds__quarter
          , subq_5.create_a_cycle_in_the_join_graph__ds__year
          , subq_5.create_a_cycle_in_the_join_graph__ds_partitioned
          , subq_5.create_a_cycle_in_the_join_graph__ds_partitioned__week
          , subq_5.create_a_cycle_in_the_join_graph__ds_partitioned__month
          , subq_5.create_a_cycle_in_the_join_graph__ds_partitioned__quarter
          , subq_5.create_a_cycle_in_the_join_graph__ds_partitioned__year
          , subq_5.create_a_cycle_in_the_join_graph__booking_paid_at
          , subq_5.create_a_cycle_in_the_join_graph__booking_paid_at__week
          , subq_5.create_a_cycle_in_the_join_graph__booking_paid_at__month
          , subq_5.create_a_cycle_in_the_join_graph__booking_paid_at__quarter
          , subq_5.create_a_cycle_in_the_join_graph__booking_paid_at__year
          , subq_5.booking_paid_at AS metric_time
          , subq_5.booking_paid_at__week AS metric_time__week
          , subq_5.booking_paid_at__month AS metric_time__month
          , subq_5.booking_paid_at__quarter AS metric_time__quarter
          , subq_5.booking_paid_at__year AS metric_time__year
          , subq_5.listing
          , subq_5.guest
          , subq_5.host
          , subq_5.create_a_cycle_in_the_join_graph
          , subq_5.create_a_cycle_in_the_join_graph__listing
          , subq_5.create_a_cycle_in_the_join_graph__guest
          , subq_5.create_a_cycle_in_the_join_graph__host
          , subq_5.is_instant
          , subq_5.create_a_cycle_in_the_join_graph__is_instant
          , subq_5.booking_payments
        FROM (
          -- Read Elements From Semantic Model 'bookings_source'
          SELECT
            1 AS bookings
            , CASE WHEN is_instant THEN 1 ELSE 0 END AS instant_bookings
            , bookings_source_src_10001.booking_value
            , bookings_source_src_10001.booking_value AS max_booking_value
            , bookings_source_src_10001.booking_value AS min_booking_value
            , bookings_source_src_10001.guest_id AS bookers
            , bookings_source_src_10001.booking_value AS average_booking_value
            , bookings_source_src_10001.booking_value AS booking_payments
            , CASE WHEN referrer_id IS NOT NULL THEN 1 ELSE 0 END AS referred_bookings
            , bookings_source_src_10001.booking_value AS median_booking_value
            , bookings_source_src_10001.booking_value AS booking_value_p99
            , bookings_source_src_10001.booking_value AS discrete_booking_value_p99
            , bookings_source_src_10001.booking_value AS approximate_continuous_booking_value_p99
            , bookings_source_src_10001.booking_value AS approximate_discrete_booking_value_p99
            , bookings_source_src_10001.is_instant
            , bookings_source_src_10001.ds
            , DATE_TRUNC(bookings_source_src_10001.ds, isoweek) AS ds__week
            , DATE_TRUNC(bookings_source_src_10001.ds, month) AS ds__month
            , DATE_TRUNC(bookings_source_src_10001.ds, quarter) AS ds__quarter
            , DATE_TRUNC(bookings_source_src_10001.ds, isoyear) AS ds__year
            , bookings_source_src_10001.ds_partitioned
            , DATE_TRUNC(bookings_source_src_10001.ds_partitioned, isoweek) AS ds_partitioned__week
            , DATE_TRUNC(bookings_source_src_10001.ds_partitioned, month) AS ds_partitioned__month
            , DATE_TRUNC(bookings_source_src_10001.ds_partitioned, quarter) AS ds_partitioned__quarter
            , DATE_TRUNC(bookings_source_src_10001.ds_partitioned, isoyear) AS ds_partitioned__year
            , bookings_source_src_10001.booking_paid_at
            , DATE_TRUNC(bookings_source_src_10001.booking_paid_at, isoweek) AS booking_paid_at__week
            , DATE_TRUNC(bookings_source_src_10001.booking_paid_at, month) AS booking_paid_at__month
            , DATE_TRUNC(bookings_source_src_10001.booking_paid_at, quarter) AS booking_paid_at__quarter
            , DATE_TRUNC(bookings_source_src_10001.booking_paid_at, isoyear) AS booking_paid_at__year
            , bookings_source_src_10001.is_instant AS create_a_cycle_in_the_join_graph__is_instant
            , bookings_source_src_10001.ds AS create_a_cycle_in_the_join_graph__ds
            , DATE_TRUNC(bookings_source_src_10001.ds, isoweek) AS create_a_cycle_in_the_join_graph__ds__week
            , DATE_TRUNC(bookings_source_src_10001.ds, month) AS create_a_cycle_in_the_join_graph__ds__month
            , DATE_TRUNC(bookings_source_src_10001.ds, quarter) AS create_a_cycle_in_the_join_graph__ds__quarter
            , DATE_TRUNC(bookings_source_src_10001.ds, isoyear) AS create_a_cycle_in_the_join_graph__ds__year
            , bookings_source_src_10001.ds_partitioned AS create_a_cycle_in_the_join_graph__ds_partitioned
            , DATE_TRUNC(bookings_source_src_10001.ds_partitioned, isoweek) AS create_a_cycle_in_the_join_graph__ds_partitioned__week
            , DATE_TRUNC(bookings_source_src_10001.ds_partitioned, month) AS create_a_cycle_in_the_join_graph__ds_partitioned__month
            , DATE_TRUNC(bookings_source_src_10001.ds_partitioned, quarter) AS create_a_cycle_in_the_join_graph__ds_partitioned__quarter
            , DATE_TRUNC(bookings_source_src_10001.ds_partitioned, isoyear) AS create_a_cycle_in_the_join_graph__ds_partitioned__year
            , bookings_source_src_10001.booking_paid_at AS create_a_cycle_in_the_join_graph__booking_paid_at
            , DATE_TRUNC(bookings_source_src_10001.booking_paid_at, isoweek) AS create_a_cycle_in_the_join_graph__booking_paid_at__week
            , DATE_TRUNC(bookings_source_src_10001.booking_paid_at, month) AS create_a_cycle_in_the_join_graph__booking_paid_at__month
            , DATE_TRUNC(bookings_source_src_10001.booking_paid_at, quarter) AS create_a_cycle_in_the_join_graph__booking_paid_at__quarter
            , DATE_TRUNC(bookings_source_src_10001.booking_paid_at, isoyear) AS create_a_cycle_in_the_join_graph__booking_paid_at__year
            , bookings_source_src_10001.listing_id AS listing
            , bookings_source_src_10001.guest_id AS guest
            , bookings_source_src_10001.host_id AS host
            , bookings_source_src_10001.guest_id AS create_a_cycle_in_the_join_graph
            , bookings_source_src_10001.listing_id AS create_a_cycle_in_the_join_graph__listing
            , bookings_source_src_10001.guest_id AS create_a_cycle_in_the_join_graph__guest
            , bookings_source_src_10001.host_id AS create_a_cycle_in_the_join_graph__host
          FROM ***************************.fct_bookings bookings_source_src_10001
        ) subq_5
      ) subq_6
    ) subq_7
    GROUP BY
      metric_time
  ) subq_8
) subq_9
ON
  subq_4.metric_time = subq_9.metric_time
GROUP BY
  metric_time
