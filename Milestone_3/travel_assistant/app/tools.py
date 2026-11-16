import json

from langchain_core.tools import tool

from app.db import get_trip_by_id
from app.weather import get_weather_forecast


@tool
def trip_lookup(trip_id: int) -> str:
    """Retrieve saved employee trip details from SQLite using the trip ID."""
    trip = get_trip_by_id(trip_id)
    if trip is None:
        return json.dumps({"status": "error", "message": "Trip not found."})
    return json.dumps({"status": "ok", "trip": trip}, ensure_ascii=False)


@tool
def weather_lookup(destination: str, start_date: str, end_date: str) -> str:
    """Look up a destination and retrieve its Open-Meteo forecast for the trip dates."""
    result = get_weather_forecast(destination, start_date, end_date)
    return json.dumps(result, ensure_ascii=False)
