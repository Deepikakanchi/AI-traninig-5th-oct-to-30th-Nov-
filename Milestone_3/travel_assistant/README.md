# AI-Powered Travel & Weather Advisory Assistant

A small FastAPI service for saving employee trips and answering travel questions using saved trip details and live Open-Meteo forecasts. LangChain formats the answer using a local Ollama model; Redis keeps short-lived, session-isolated chat history; SQLite stores trips and session-to-trip links.

## Project structure

```text
travel_assistant/
├── app/
│   ├── __init__.py
│   ├── config.py       # Loads .env and service settings
│   ├── db.py           # SQLite connections and trip queries
│   ├── schemas.py      # Request validation
│   ├── weather.py      # Open-Meteo geocoding and forecasts
│   ├── tools.py        # LangChain trip and weather tools
│   ├── memory.py       # Redis conversation history
│   ├── agent.py        # LangChain prompt and Ollama model
│   └── main.py         # FastAPI app and endpoints
├── schema.sql          # SQLite tables, initialized at app startup
├── seed.sql            # Optional sample trip records
├── requirements.txt
├── .env                # Local settings; contains no API key
├── .env.example
└── README.md
```

## Requirements

- Python 3.11 or newer
- Ollama installed as a Windows application, with the configured model downloaded
- Redis running at the URL configured in `.env`
- Internet access for the Open-Meteo geocoding and forecast APIs

The project uses **SQLite**, not PostgreSQL. The database file is created automatically at the path in `DATABASE_PATH` (by default, `travel_weather.db` in this project folder).

## Setup on Windows

Open PowerShell in the project directory:

```powershell
cd $HOME\Downloads\milestone_3\travel_assistant
```

Activate the existing virtual environment, or create one if needed:

```powershell
.\venv\Scripts\Activate.ps1
# If the venv does not exist:
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the Python packages:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Install and start Ollama

Ollama is a separate Windows application; installing `langchain-ollama` with pip does not install it. Install Ollama using its official Windows installer, or try:

```powershell
winget install --id Ollama.Ollama -e
```

After installation, close and reopen PowerShell, then verify the command is available and download the configured model:

```powershell
ollama --version
ollama pull qwen2.5:3b
```

If PowerShell still says `ollama` is not recognized, check whether the application exists at its usual per-user location:

```powershell
Test-Path "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
```

If that returns `True`, run it by full path to verify the installation:

```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" --version
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull qwen2.5:3b
```

If the file is absent, install Ollama first. If it is present, reopen the terminal or add its installation directory to your Windows `PATH`. Keep Ollama running locally for the assistant to use it.

### Start Redis

If Docker Desktop is installed, start a local Redis container:

```powershell
docker run --name travel-redis -p 6379:6379 -d redis
```

For later runs, start the existing container with:

```powershell
docker start travel-redis
```

Alternatively, run a Redis-compatible service locally and set its address in `.env`. The default is `redis://localhost:6379/0`.

## Configure and run

The included `.env` uses local defaults. Review it if your services use different addresses:

```dotenv
DATABASE_PATH=travel_weather.db
REDIS_URL=redis://localhost:6379/0
REDIS_SESSION_TTL_SECONDS=86400
REDIS_MAX_HISTORY_MESSAGES=10
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:3b
WEATHER_API_TIMEOUT_SECONDS=15
```

Start the API from the project directory:

```powershell
uvicorn app.main:app --reload
```

Open Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). The root endpoint at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) can be used as a basic health check.

## API endpoints

### `POST /trips`

Create and save a trip. If a `session_id` is supplied, that session is linked to the new trip.

```json
{
  "employee_id": "EMP104",
  "destination": "Jaipur",
  "start_date": "2026-11-20",
  "end_date": "2026-11-22",
  "purpose": "Client meeting",
  "session_id": "demo-session"
}
```

The response contains the new `trip_id` and saved trip.

### `GET /trips/{trip_id}`

Retrieve the saved trip, including its employee reference, destination, dates, purpose, and status.

### `POST /ask`

Ask a question about a trip. Use a `session_id` linked when creating a trip, or provide an existing `trip_id` to associate that trip with this session:

```json
{
  "session_id": "demo-session",
  "question": "What weather should I expect, and what should I pack?"
}
```

Example follow-up in the same session:

```json
{
  "session_id": "demo-session",
  "question": "Will I need an umbrella?"
}
```

For an existing trip that has not been linked to the session, include its ID:

```json
{
  "session_id": "another-session",
  "trip_id": 1,
  "question": "What should I pack?"
}
```

The response contains the answer, trip ID, weather summary, and forecast data. Redis conversation history is isolated by session ID, limited to the configured number of recent messages, and expires after the configured TTL.

## Optional sample data

`seed.sql` inserts sample trip IDs 104, 205, and 310 and links `demo-session` to trip 104. Tables are created automatically when the API starts. To add the sample rows, stop the API and run this from the project directory:

```powershell
python -c "import sqlite3; from app.config import DATABASE_PATH, PROJECT_ROOT; c=sqlite3.connect(DATABASE_PATH); c.executescript((PROJECT_ROOT / 'seed.sql').read_text(encoding='utf-8')); c.commit(); c.close()"
```

Run the seed only when those IDs are not already used by other trips in your database.

## Errors and troubleshooting

- **`422` from `/trips` or `/ask`:** check required fields, non-empty text, ISO date format (`YYYY-MM-DD`), date order, and positive trip IDs.
- **`404` from `/trips/{trip_id}`:** no saved trip has that ID.
- **`404` from `/ask`:** the trip does not exist or is not linked to the given session; create it with that `session_id` or pass `trip_id`.
- **`503` mentioning Redis:** start Redis and check `REDIS_URL`.
- **`503` mentioning Ollama:** install and start Ollama, check `OLLAMA_BASE_URL`, and confirm the model is downloaded with `ollama list`.
- **Weather unavailable:** check internet access and the destination. Forecasts are limited to the dates currently published by Open-Meteo; the assistant reports missing data rather than making up conditions.

Open-Meteo's free API is intended for non-commercial use. Follow its current usage and attribution terms.
