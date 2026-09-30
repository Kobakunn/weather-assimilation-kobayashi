CREATE OR REPLACE TABLE weather_mart.forecast_corrected AS

SELECT
    fa.time,
    fa.forecast_temp,
    fa.forecast_temp
      + COALESCE(prev_db.daily_bias, 0)
      AS corrected_temp,
    fa.actual_temp
FROM weather_mart.forecast_accuracy fa

LEFT JOIN weather_mart.daily_bias prev_db
    ON prev_db.forecast_date =
       DATE_SUB(fa.forecast_date, INTERVAL 1 DAY);