CREATE OR REPLACE TABLE weather_mart.forecast_metrics AS
SELECT
  AVG(ABS(error)) AS mae,
  SQRT(AVG(POWER(error,2))) AS rmse,
  AVG(error) AS bias
FROM weather_mart.forecast_accuracy;