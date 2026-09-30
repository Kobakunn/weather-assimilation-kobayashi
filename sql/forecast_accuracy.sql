CREATE OR REPLACE TABLE weather_mart.forecast_accuracy AS
SELECT
    f.time,
    AVG(f.temperature_2m) AS forecast_temp,
    AVG(o.temperature_2m) AS actual_temp,
    AVG(o.temperature_2m) - AVG(f.temperature_2m) AS error,
    DATE(f.time) AS forecast_date
FROM weather_stg.forecast_hourly f
JOIN weather_stg.observation_hourly o
    ON f.time = o.time
GROUP BY
    f.time,
    DATE(f.time);