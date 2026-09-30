CREATE OR REPLACE TABLE weather_mart.daily_bias AS
SELECT
    forecast_date,
    AVG(error) AS daily_bias
FROM weather_mart.forecast_accuracy
GROUP BY forecast_date;