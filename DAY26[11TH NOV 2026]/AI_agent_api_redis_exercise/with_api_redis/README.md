# Employee Leave Support Agent API (FastAPI + Redis)

This project exposes the existing Microsoft Foundry `EmployeeLeaveAgent` as a
FastAPI service. Redis stores conversation IDs and chat history for up to one
hour.

## Requirements

- Windows
- Python 3.14 (recommended; dependencies may not yet install cleanly on Python
  3.16)
- Docker Desktop
- Azure CLI
- Access to the Microsoft Foundry project and agent

## Configuration

The `.env` file in this folder should contain:

```dotenv
FOUNDRY_PROJECT_ENDPOINT=<your Microsoft Foundry project endpoint>
FOUNDRY_AGENT_NAME=EmployeeLeaveAgent
REDIS_URL=redis://localhost:6379/0
```

Keep `.env` private; do not commit credentials or secrets to source control.

## Setup

Open PowerShell in this project folder and create a virtual environment,
install the packages, and sign in to Azure:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
az login
```

If PowerShell blocks activation, allow it for the current terminal session and
activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

If `py -3.14` is not available, select your installed Python 3.14 interpreter
in VS Code and use that interpreter to create the virtual environment and
install the requirements.

## Start Redis

Keep Docker Desktop running. Start Redis in a separate PowerShell window:

```powershell
docker run -d --name retail-redis -p 127.0.0.1:6379:6379 -v retail_redis_data:/data redis:7-alpine redis-server --appendonly yes
docker exec retail-redis redis-cli ping
```

The ping command should print `PONG`. If the container already exists, start it
instead of creating it again:

```powershell
docker start retail-redis
docker exec retail-redis redis-cli ping
```

## Run the API

In the project folder, with the virtual environment activated, run:

```powershell
python -m uvicorn main:app --reload
```

Open the interactive API documentation at
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Keep this terminal
running while using the API. Press `Ctrl+C` to stop it.

## Use the API

In `/docs`, expand **POST `/chat`**, choose **Try it out**, and send:

```json
{
  "message": "How do I request annual leave?"
}
```

`session_id` is optional. The response includes a `session_id` and the agent's
`reply`. To continue an existing session, send its returned ID:

```json
{
  "message": "How many days can I take?",
  "session_id": "paste-the-session-id-here"
}
```

Use **GET `/history/{session_id}`** with that ID to retrieve the stored chat
history. The API also serves its OpenAPI schema at
[http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json).

## Troubleshooting

- **Missing Python package:** activate this project's `.venv` and run
  `python -m pip install -r requirements.txt` from this folder.
- **Redis connection error:** make sure Docker is running and
  `docker exec retail-redis redis-cli ping` returns `PONG`.
- **Azure authentication error:** run `az login` and confirm the signed-in
  account can access the configured Foundry project and agent.
- **Port 8000 is in use:** stop the other process using the port or start
  Uvicorn on another port, for example
  `python -m uvicorn main:app --reload --port 8001`.
