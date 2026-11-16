from datetime import date
from typing import Any

import requests

from app.config import WEATHER_API_TIMEOUT_SECONDS

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather_forecast(destination: str, start_date: str, end_date: str) -> dict[str, Any]:
    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
        if end < start:
            return {"status": "error", "message": "The trip end date is before its start date."}
    except ValueError:
        return {"status": "error", "message": "Trip dates must use YYYY-MM-DD format."}

    try:
        geocoding_response = requests.get(
            GEOCODING_URL,
            params={"name": destination, "count": 1, "language": "en", "format": "json"},
            timeout=WEATHER_API_TIMEOUT_SECONDS,
        )
        geocoding_response.raise_for_status()
        locations = geocoding_response.json().get("results") or []
    except (requests.RequestException, ValueError) as exc:
        return {"status": "error", "message": f"Could not look up destination: {exc}"}

    if not locations:
        return {"status": "error", "message": f"Destination '{destination}' was not found."}

    location = locations[0]
    try:
        forecast_response = requests.get(
            FORECAST_URL,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "timezone": location.get("timezone", "auto"),
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
                "daily": (
                    "temperature_2m_max,temperature_2m_min,"
                    "precipitation_probability_max"
                ),
            },
            timeout=WEATHER_API_TIMEOUT_SECONDS,
        )
        forecast_response.raise_for_status()
        daily = forecast_response.json().get("daily") or {}
    except (KeyError, requests.RequestException, ValueError) as exc:
        return {"status": "error", "message": f"Could not retrieve the forecast: {exc}"}

    dates = daily.get("time") or []
    if not dates:
        return {
            "status": "error",
            "message": (
                "The weather provider has no forecast for those dates. "
                "They may be outside its published forecast horizon."
            ),
        }

    highs = daily.get("temperature_2m_max") or []
    lows = daily.get("temperature_2m_min") or []
    precipitation = daily.get("precipitation_probability_max") or []
    forecast = [
        {
            "date": day,
            "max_temp_c": highs[index] if index < len(highs) else None,
            "min_temp_c": lows[index] if index < len(lows) else None,
            "precipitation_probability_percent": (
                precipitation[index] if index < len(precipitation) else None
            ),
        }
        for index, day in enumerate(dates)
    ]

    valid_highs = [item["max_temp_c"] for item in forecast if item["max_temp_c"] is not None]
    valid_lows = [item["min_temp_c"] for item in forecast if item["min_temp_c"] is not None]
    valid_precipitation = [
        item["precipitation_probability_percent"]
        for item in forecast
        if item["precipitation_probability_percent"] is not None
    ]

    summary_parts = []
    if valid_highs:
        summary_parts.append(f"daily highs {min(valid_highs):g}-{max(valid_highs):g} C")
    if valid_lows:
        summary_parts.append(f"daily lows {min(valid_lows):g}-{max(valid_lows):g} C")
    if valid_precipitation:
        summary_parts.append(
            f"precipitation chance {min(valid_precipitation):g}-{max(valid_precipitation):g}%"
        )

    return {
        "status": "ok",
        "destination": location.get("name", destination),
        "country": location.get("country"),
        "timezone": location.get("timezone"),
        "summary": "; ".join(summary_parts) if summary_parts else "No weather values were returned.",
        "forecast": forecast,
    }
