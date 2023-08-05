-- Order By ['listing__country_latest'] Limit 100
SELECT
  subq_10.listing__country_latest
FROM (
  -- Pass Only Elements:
  --   ['listing__country_latest']
  SELECT
    subq_9.listing__country_latest
  FROM (
    -- Compute Metrics via Expressions
    SELECT
      subq_8.bookings
      , subq_8.listing__country_latest
    FROM (
      -- Aggregate Measures
      SELECT
        SUM(subq_7.bookings) AS bookings
        , subq_7.listing__country_latest
      FROM (
        -- Pass Only Elements:
        --   ['bookings', 'listing__country_latest']
        SELECT
          subq_6.bookings
          , subq_6.listing__country_latest
        FROM (
          -- Join Standard Outputs
          SELECT
            subq_2.bookings AS bookings
            , subq_5.country_latest AS listing__country_latest
            , subq_2.listing AS listing
          FROM (
            -- Pass Only Elements:
            --   ['bookings', 'listing']
            SELECT
              subq_1.bookings
              , subq_1.listing
            FROM (
              -- Metric Time Dimension 'ds'
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
          LEFT OUTER JOIN (
            -- Pass Only Elements:
            --   ['listing', 'country_latest']
            SELECT
              subq_4.country_latest
              , subq_4.listing
            FROM (
              -- Metric Time Dimension 'ds'
              SELECT
                subq_3.listings
                , subq_3.largest_listing
                , subq_3.smallest_listing
                , subq_3.country_latest
                , subq_3.is_lux_latest
                , subq_3.capacity_latest
                , subq_3.listing__country_latest
                , subq_3.listing__is_lux_latest
                , subq_3.listing__capacity_latest
                , subq_3.ds
                , subq_3.ds__week
                , subq_3.ds__month
                , subq_3.ds__quarter
                , subq_3.ds__year
                , subq_3.created_at
                , subq_3.created_at__week
                , subq_3.created_at__month
                , subq_3.created_at__quarter
                , subq_3.created_at__year
                , subq_3.listing__ds
                , subq_3.listing__ds__week
                , subq_3.listing__ds__month
                , subq_3.listing__ds__quarter
                , subq_3.listing__ds__year
                , subq_3.listing__created_at
                , subq_3.listing__created_at__week
                , subq_3.listing__created_at__month
                , subq_3.listing__created_at__quarter
                , subq_3.listing__created_at__year
                , subq_3.ds AS metric_time
                , subq_3.ds__week AS metric_time__week
                , subq_3.ds__month AS metric_time__month
                , subq_3.ds__quarter AS metric_time__quarter
                , subq_3.ds__year AS metric_time__year
                , subq_3.listing
                , subq_3.user
                , subq_3.listing__user
              FROM (
                -- Read Elements From Data Source 'listings_latest'
                SELECT
                  1 AS listings
                  , listings_latest_src_10003.capacity AS largest_listing
                  , listings_latest_src_10003.capacity AS smallest_listing
                  , listings_latest_src_10003.created_at AS ds
                  , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds__week
                  , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds__month
                  , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds__quarter
                  , '__DATE_TRUNC_NOT_SUPPORTED__' AS ds__year
                  , listings_latest_src_10003.created_at
                  , '__DATE_TRUNC_NOT_SUPPORTED__' AS created_at__week
                  , '__DATE_TRUNC_NOT_SUPPORTED__' AS created_at__month
                  , '__DATE_TRUNC_NOT_SUPPORTED__' AS created_at__quarter
                  , '__DATE_TRUNC_NOT_SUPPORTED__' AS created_at__year
                  , listings_latest_src_10003.country AS country_latest
                  , listings_latest_src_10003.is_lux AS is_lux_latest
                  , listings_latest_src_10003.capacity AS capacity_latest
                  , listings_latest_src_10003.created_at AS listing__ds
                  , '__DATE_TRUNC_NOT_SUPPORTED__' AS listing__ds__week
                  , '__DATE_TRUNC_NOT_SUPPORTED__' AS listing__ds__month
                  , '__DATE_TRUNC_NOT_SUPPORTED__' AS listing__ds__quarter
                  , '__DATE_TRUNC_NOT_SUPPORTED__' AS listing__ds__year
                  , listings_latest_src_10003.created_at AS listing__created_at
                  , '__DATE_TRUNC_NOT_SUPPORTED__' AS listing__created_at__week
                  , '__DATE_TRUNC_NOT_SUPPORTED__' AS listing__created_at__month
                  , '__DATE_TRUNC_NOT_SUPPORTED__' AS listing__created_at__quarter
                  , '__DATE_TRUNC_NOT_SUPPORTED__' AS listing__created_at__year
                  , listings_latest_src_10003.country AS listing__country_latest
                  , listings_latest_src_10003.is_lux AS listing__is_lux_latest
                  , listings_latest_src_10003.capacity AS listing__capacity_latest
                  , listings_latest_src_10003.listing_id AS listing
                  , listings_latest_src_10003.user_id AS user
                  , listings_latest_src_10003.user_id AS listing__user
                FROM ***************************.dim_listings_latest listings_latest_src_10003
              ) subq_3
            ) subq_4
          ) subq_5
          ON
            subq_2.listing = subq_5.listing
        ) subq_6
      ) subq_7
      GROUP BY
        subq_7.listing__country_latest
    ) subq_8
  ) subq_9
) subq_10
ORDER BY subq_10.listing__country_latest
LIMIT 100
