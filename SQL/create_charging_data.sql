CREATE OR REPLACE TABLE charging_data AS

SELECT
    c.start_time,
    c.end_time,
    c.carbon_forecast,
    c.carbon_actual,
    c.carbon_index,
    p.price_p_per_kwh

FROM carbon_intensity AS c

INNER JOIN electricity_prices AS p
    ON c.start_time = p.start_time
    AND c.end_time = p.end_time

ORDER BY c.start_time;