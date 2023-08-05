-- Combine Metrics
SELECT
  subq_8.bookings AS bookings
  , subq_9.booking_payments AS booking_payments
  , COALESCE(subq_8._ts, subq_9._ts) AS _ts
FROM (
  -- Compute Metrics via Expressions
  SELECT
    subq_3.bookings
    , subq_3._ts
  FROM (
    -- Aggregate Measures
    SELECT
      SUM(subq_2.bookings) AS bookings
      , subq_2._ts
    FROM (
      -- Pass Only Elements:
      --   ['bookings', '_ts']
      SELECT
        subq_1.bookings
        , subq_1._ts
      FROM (
        -- Plot by Time Dimension 'ds'
        SELECT
          subq_0.bookings
          , subq_0.instant_bookings
          , subq_0.booking_value
          , subq_0.max_booking_value
          , subq_0.min_booking_value
          , subq_0.bookers
          , subq_0.average_booking_value
          , subq_0.is_instant
          , subq_0.create_a_cycle_in_the_join_graph__is_instant
          , subq_0.ds
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
          , subq_0.ds AS _ts
          , subq_0.ds__week AS _ts__week
          , subq_0.ds__month AS _ts__month
          , subq_0.ds__quarter AS _ts__quarter
          , subq_0.ds__year AS _ts__year
          , subq_0.listing
          , subq_0.guest
          , subq_0.host
          , subq_0.create_a_cycle_in_the_join_graph
          , subq_0.create_a_cycle_in_the_join_graph__listing
          , subq_0.create_a_cycle_in_the_join_graph__guest
          , subq_0.create_a_cycle_in_the_join_graph__host
        FROM (
          -- Read Elements From Data Source 'bookings_source'
          SELECT
            1 AS bookings
            , CASE WHEN is_instant THEN 1 ELSE 0 END AS instant_bookings
            , bookings_source_src_10000.booking_value
            , bookings_source_src_10000.booking_value AS max_booking_value
            , bookings_source_src_10000.booking_value AS min_booking_value
            , bookings_source_src_10000.guest_id AS bookers
            , bookings_source_src_10000.booking_value AS average_booking_value
            , bookings_source_src_10000.booking_value AS booking_payments
            , bookings_source_src_10000.is_instant
            , bookings_source_src_10000.ds
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds__week
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds__month
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds__quarter
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds__year
            , bookings_source_src_10000.ds_partitioned
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds_partitioned__week
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds_partitioned__month
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds_partitioned__quarter
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds_partitioned__year
            , bookings_source_src_10000.booking_paid_at
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS booking_paid_at__week
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS booking_paid_at__month
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS booking_paid_at__quarter
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS booking_paid_at__year
            , bookings_source_src_10000.is_instant AS create_a_cycle_in_the_join_graph__is_instant
            , bookings_source_src_10000.ds AS create_a_cycle_in_the_join_graph__ds
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__ds__week
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__ds__month
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__ds__quarter
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__ds__year
            , bookings_source_src_10000.ds_partitioned AS create_a_cycle_in_the_join_graph__ds_partitioned
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__ds_partitioned__week
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__ds_partitioned__month
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__ds_partitioned__quarter
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__ds_partitioned__year
            , bookings_source_src_10000.booking_paid_at AS create_a_cycle_in_the_join_graph__booking_paid_at
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__booking_paid_at__week
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__booking_paid_at__month
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__booking_paid_at__quarter
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__booking_paid_at__year
            , bookings_source_src_10000.listing_id AS listing
            , bookings_source_src_10000.guest_id AS guest
            , bookings_source_src_10000.host_id AS host
            , bookings_source_src_10000.guest_id AS create_a_cycle_in_the_join_graph
            , bookings_source_src_10000.listing_id AS create_a_cycle_in_the_join_graph__listing
            , bookings_source_src_10000.guest_id AS create_a_cycle_in_the_join_graph__guest
            , bookings_source_src_10000.host_id AS create_a_cycle_in_the_join_graph__host
          FROM (
            -- User Defined SQL Query
            SELECT * FROM ***************************.fct_bookings
          ) bookings_source_src_10000
        ) subq_0
      ) subq_1
    ) subq_2
    GROUP BY
      subq_2._ts
  ) subq_3
) subq_8
FULL OUTER JOIN (
  -- Compute Metrics via Expressions
  SELECT
    subq_7.booking_payments
    , subq_7._ts
  FROM (
    -- Aggregate Measures
    SELECT
      SUM(subq_6.booking_payments) AS booking_payments
      , subq_6._ts
    FROM (
      -- Pass Only Elements:
      --   ['booking_payments', '_ts']
      SELECT
        subq_5.booking_payments
        , subq_5._ts
      FROM (
        -- Plot by Time Dimension 'booking_paid_at'
        SELECT
          subq_4.booking_payments
          , subq_4.is_instant
          , subq_4.create_a_cycle_in_the_join_graph__is_instant
          , subq_4.ds
          , subq_4.ds__week
          , subq_4.ds__month
          , subq_4.ds__quarter
          , subq_4.ds__year
          , subq_4.ds_partitioned
          , subq_4.ds_partitioned__week
          , subq_4.ds_partitioned__month
          , subq_4.ds_partitioned__quarter
          , subq_4.ds_partitioned__year
          , subq_4.booking_paid_at
          , subq_4.booking_paid_at__week
          , subq_4.booking_paid_at__month
          , subq_4.booking_paid_at__quarter
          , subq_4.booking_paid_at__year
          , subq_4.create_a_cycle_in_the_join_graph__ds
          , subq_4.create_a_cycle_in_the_join_graph__ds__week
          , subq_4.create_a_cycle_in_the_join_graph__ds__month
          , subq_4.create_a_cycle_in_the_join_graph__ds__quarter
          , subq_4.create_a_cycle_in_the_join_graph__ds__year
          , subq_4.create_a_cycle_in_the_join_graph__ds_partitioned
          , subq_4.create_a_cycle_in_the_join_graph__ds_partitioned__week
          , subq_4.create_a_cycle_in_the_join_graph__ds_partitioned__month
          , subq_4.create_a_cycle_in_the_join_graph__ds_partitioned__quarter
          , subq_4.create_a_cycle_in_the_join_graph__ds_partitioned__year
          , subq_4.create_a_cycle_in_the_join_graph__booking_paid_at
          , subq_4.create_a_cycle_in_the_join_graph__booking_paid_at__week
          , subq_4.create_a_cycle_in_the_join_graph__booking_paid_at__month
          , subq_4.create_a_cycle_in_the_join_graph__booking_paid_at__quarter
          , subq_4.create_a_cycle_in_the_join_graph__booking_paid_at__year
          , subq_4.booking_paid_at AS _ts
          , subq_4.booking_paid_at__week AS _ts__week
          , subq_4.booking_paid_at__month AS _ts__month
          , subq_4.booking_paid_at__quarter AS _ts__quarter
          , subq_4.booking_paid_at__year AS _ts__year
          , subq_4.listing
          , subq_4.guest
          , subq_4.host
          , subq_4.create_a_cycle_in_the_join_graph
          , subq_4.create_a_cycle_in_the_join_graph__listing
          , subq_4.create_a_cycle_in_the_join_graph__guest
          , subq_4.create_a_cycle_in_the_join_graph__host
        FROM (
          -- Read Elements From Data Source 'bookings_source'
          SELECT
            1 AS bookings
            , CASE WHEN is_instant THEN 1 ELSE 0 END AS instant_bookings
            , bookings_source_src_10000.booking_value
            , bookings_source_src_10000.booking_value AS max_booking_value
            , bookings_source_src_10000.booking_value AS min_booking_value
            , bookings_source_src_10000.guest_id AS bookers
            , bookings_source_src_10000.booking_value AS average_booking_value
            , bookings_source_src_10000.booking_value AS booking_payments
            , bookings_source_src_10000.is_instant
            , bookings_source_src_10000.ds
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds__week
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds__month
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds__quarter
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds__year
            , bookings_source_src_10000.ds_partitioned
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds_partitioned__week
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds_partitioned__month
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds_partitioned__quarter
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds_partitioned__year
            , bookings_source_src_10000.booking_paid_at
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS booking_paid_at__week
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS booking_paid_at__month
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS booking_paid_at__quarter
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS booking_paid_at__year
            , bookings_source_src_10000.is_instant AS create_a_cycle_in_the_join_graph__is_instant
            , bookings_source_src_10000.ds AS create_a_cycle_in_the_join_graph__ds
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__ds__week
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__ds__month
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__ds__quarter
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__ds__year
            , bookings_source_src_10000.ds_partitioned AS create_a_cycle_in_the_join_graph__ds_partitioned
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__ds_partitioned__week
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__ds_partitioned__month
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__ds_partitioned__quarter
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__ds_partitioned__year
            , bookings_source_src_10000.booking_paid_at AS create_a_cycle_in_the_join_graph__booking_paid_at
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__booking_paid_at__week
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__booking_paid_at__month
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__booking_paid_at__quarter
            , '__DATE_TRUNC_NOT_SUPPORTED__' AS create_a_cycle_in_the_join_graph__booking_paid_at__year
            , bookings_source_src_10000.listing_id AS listing
            , bookings_source_src_10000.guest_id AS guest
            , bookings_source_src_10000.host_id AS host
            , bookings_source_src_10000.guest_id AS create_a_cycle_in_the_join_graph
            , bookings_source_src_10000.listing_id AS create_a_cycle_in_the_join_graph__listing
            , bookings_source_src_10000.guest_id AS create_a_cycle_in_the_join_graph__guest
            , bookings_source_src_10000.host_id AS create_a_cycle_in_the_join_graph__host
          FROM (
            -- User Defined SQL Query
            SELECT * FROM ***************************.fct_bookings
          ) bookings_source_src_10000
        ) subq_4
      ) subq_5
    ) subq_6
    GROUP BY
      subq_6._ts
  ) subq_7
) subq_9
ON
  subq_8._ts = subq_9._ts
