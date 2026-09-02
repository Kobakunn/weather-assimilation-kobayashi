import json
import pandas as pd

with open("observation.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame({
    "time": data["hourly"]["time"],
    "temperature_2m": data["hourly"]["temperature_2m"]
})

df.to_csv("observation_hourly.csv", index=False)