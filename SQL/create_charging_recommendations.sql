CREATE OR REPLACE TABLE charging_recommendations AS

WITH ranked_periods AS (
    SELECT
        *,
        RANK() OVER (ORDER BY price_p_per_kwh ASC) AS price_rank,
        RANK() OVER (ORDER BY carbon_forecast ASC) AS carbon_rank
    FROM charging_data
)

SELECT
    *,
    price_rank + carbon_rank AS charging_score
FROM ranked_periods
ORDER BY charging_score ASC;