import requests
import json

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from google.cloud import storage, bigquery


def weather_data_fetch(request):

    storage_client = storage.Client()
    bq_client = bigquery.Client()
    bucket = storage_client.bucket("weather-assimilation")

    # Forecast API
    forecast_url = "https://api.open-meteo.com/v1/forecast"

    forecast_params = {
        "latitude": 35.68,
        "longitude": 139.76,
        "hourly": "temperature_2m",
        "forecast_days": 1,
        "timezone": "Asia/Tokyo"
    }

    forecast_data = requests.get(
        forecast_url,
        params=forecast_params
    ).json()

    # Archive API
    yesterday = (datetime.now(ZoneInfo("Asia/Tokyo")) - timedelta(days=1)).strftime("%Y-%m-%d")
    today_name = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y%m%d")
    yesterday_name = (datetime.now(ZoneInfo("Asia/Tokyo")) - timedelta(days=1)).strftime("%Y%m%d")

    forecast_blob = bucket.blob(
        f"raw/forecast/{today_name}_forecast.json"
    )

    forecast_blob.upload_from_string(
        json.dumps(forecast_data),
        content_type="application/json"
    )

    forecast_rows = []

    for time, temp in zip(
        forecast_data["hourly"]["time"],
        forecast_data["hourly"]["temperature_2m"]
    ):
        forecast_rows.append({
            "time": time,
            "temperature_2m": temp
        })

    forecast_table_id = (
        "weather-assimilation-kobayashi.weather_stg.forecast_hourly"
    )

    forecast_errors = bq_client.insert_rows_json(
        forecast_table_id,
        forecast_rows
    )

    if forecast_errors:
        print(f"Forecast Error: {forecast_errors}")
    else:
        print("Forecast inserted successfully")

    observation_url = (
        "https://archive-api.open-meteo.com/v1/archive"
    )

    observation_params = {
        "latitude": 35.68,
        "longitude": 139.76,
        "start_date": yesterday,
        "end_date": yesterday,
        "hourly": "temperature_2m"
    }

    observation_data = requests.get(
        observation_url,
        params=observation_params
    ).json()

    observation_blob = bucket.blob(
        f"raw/observation/{yesterday_name}_observation.json"
    )

    observation_blob.upload_from_string(
        json.dumps(observation_data),
        content_type="application/json"
    )

    observation_rows = []

    for time, temp in zip(
        observation_data["hourly"]["time"],
        observation_data["hourly"]["temperature_2m"]
    ):
        observation_rows.append({
            "time": time,
            "temperature_2m": temp
        })

    observation_table_id = (
        "weather-assimilation-kobayashi.weather_stg.observation_hourly"
    )

    observation_errors = bq_client.insert_rows_json(
        observation_table_id,
        observation_rows
    )

    if observation_errors:
        print(f"Observation Error: {observation_errors}")
    else:
        print("Observation inserted successfully")

    print(datetime.now(ZoneInfo("Asia/Tokyo")))
    print(yesterday)

    return "success"