# Employee Leave Support Agent (CLI + FastAPI + Redis)

An extended exercise that applies the Day 26 pattern to a new business case: an **HR assistant** that answers employee leave questions. It connects to the `EmployeeLeaveAgent` in a **Microsoft Foundry (Azure AI Foundry)** project and is built in two versions:

1. **CLI version** – chat with the agent from the terminal
2. **API version** – FastAPI service with Redis-backed session memory

> Part of the AI Training Program – Day 26 (11 Nov 2026)

---

## Table of Contents

1. [Use Case](#use-case)
2. [CLI vs API](#cli-vs-api)
3. [Architecture](#architecture)
4. [Project Structure](#project-structure)
5. [Requirements](#requirements)
6. [Configuration](#configuration)
7. [Setup](#setup)
8. [Part 1 – CLI Version](#part-1--cli-version)
9. [Part 2 – API Version](#part-2--api-version)
10. [API Reference](#api-reference)
11. [Sample Questions](#sample-questions)
12. [Troubleshooting](#troubleshooting)
13. [What This Exercise Teaches](#what-this-exercise-teaches)
14. [Security Notes](#security-notes)
15. [Possible Improvements](#possible-improvements)

---

## Use Case

Employees often ask HR the same questions: how to apply for leave, how many days they get, which leave types exist. `EmployeeLeaveAgent` answers these questions using the instructions (and any policy documents) configured in Foundry, freeing HR from repetitive queries.

---

## CLI vs API

| | CLI version | API version |
|---|---|---|
| Interface | Terminal | HTTP (`/chat`, `/history`) |
| Users | One person | Many sessions at once |
| Memory | Only while the terminal is open | Stored in Redis for 1 hour |
| Redis needed | No | Yes |
| Best for | Quick testing | Integrating into apps / frontends |

---

## Architecture

**CLI**

```text
 You (terminal) ──► main.py ──► AIProjectClient ──► EmployeeLeaveAgent
        ▲                                                │
        └──────────────────── reply ◄────────────────────┘
```

**API**

```text
 Client (Swagger / Postman / Frontend)
        │ POST /chat
        ▼
 FastAPI (main.py) ◄──► Redis (conversation ID + history, 1 hour)
        │
        ▼
 Microsoft Foundry project ──► EmployeeLeaveAgent
```

---

## Project Structure

```text
AI_agent_api_redis_exercise/
├── main.py            # App entry point (CLI or FastAPI version)
├── requirements.txt   # Python dependencies
├── README.md          # This file
├── .env               # Local settings (NOT committed)
└── .venv/             # Virtual environment (NOT committed)
```

---

## Requirements

- Windows 10 or later with PowerShell
- Python 3.14 recommended (3.16 may not install dependencies cleanly)
- Azure CLI, available in `PATH`
- Access to a Foundry project containing `EmployeeLeaveAgent`
- Docker Desktop (**API version only**)

### Dependencies

| Package | CLI | API | Purpose |
|---|:-:|:-:|---|
| `azure-ai-projects` | ✓ | ✓ | Foundry project and agent client |
| `azure-identity` | ✓ | ✓ | Azure authentication |
| `python-dotenv` | ✓ | ✓ | Loads `.env` |
| `fastapi` | | ✓ | Web framework |
| `uvicorn` | | ✓ | Runs the API server |
| `redis` | | ✓ | Session storage |

---

## Configuration

Create `.env` in the same folder as `main.py`:

```dotenv
FOUNDRY_PROJECT_ENDPOINT=https://<your-resource>.services.ai.azure.com/api/projects/<project-name>
FOUNDRY_AGENT_NAME=EmployeeLeaveAgent
REDIS_URL=redis://localhost:6379/0
```

| Variable | Needed for | Description |
|---|---|---|
| `FOUNDRY_PROJECT_ENDPOINT` | CLI + API | Foundry project endpoint from the portal |
| `FOUNDRY_AGENT_NAME` | CLI + API | Must match the agent name exactly |
| `REDIS_URL` | API only | Redis connection string |

---

## Setup

### 1. Create and activate a virtual environment

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation is blocked:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

If `py -3.14` is not available, select your Python 3.14 interpreter in VS Code and use it.

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Sign in to Azure

```powershell
az login
az account list -o table
az account set --subscription "<subscription-name-or-id>"   # if you have several
```

---

## Part 1 – CLI Version

### Run

```powershell
python main.py
```

### Example session

```text
Connected to EmployeeLeaveAgent
Type exit to quit

You: How many days of annual leave do employees get?
Agent: Employees are entitled to ...

You: How do I apply for it?
Agent: To apply for annual leave, ...

You: exit
```

### How it works

1. `load_dotenv()` loads `.env`.
2. `AIProjectClient` is created with the endpoint, `DefaultAzureCredential()` and `allow_preview=True`.
3. `project.get_openai_client()` returns a client for the named agent.
4. `client.conversations.create()` starts one conversation.
5. Each question is sent with `client.responses.create(...)` in that conversation.
6. `response.output_text` is printed.
7. Typing `exit` ends the program.

---

## Part 2 – API Version

### 1. Start Redis

Keep Docker Desktop running and, in a separate terminal:

```powershell
docker run -d --name retail-redis -p 127.0.0.1:6379:6379 -v retail_redis_data:/data redis:7-alpine redis-server --appendonly yes
docker exec retail-redis redis-cli ping
```

You should see `PONG`. If the container already exists:

```powershell
docker start retail-redis
docker exec retail-redis redis-cli ping
```

### 2. Start the API

```powershell
python -m uvicorn main:app --reload
```

Open:

- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI schema: http://127.0.0.1:8000/openapi.json

Keep this terminal open. Press `Ctrl+C` to stop.

### 3. Try it in Swagger

1. Expand **POST `/chat`** → **Try it out**.
2. Send:

   ```json
   { "message": "How do I request annual leave?" }
   ```

3. Copy the `session_id` from the response.
4. Continue the conversation:

   ```json
   {
     "message": "How many days can I take?",
     "session_id": "paste-the-session-id-here"
   }
   ```

5. Use **GET `/history/{session_id}`** to see the full history.

### How the API works

1. The request is validated by a Pydantic model.
2. A `session_id` is generated if none was sent.
3. Redis is checked for that session's Foundry conversation ID; a new conversation is created if missing.
4. The message is sent to `EmployeeLeaveAgent`.
5. Both the question and the reply are added to the session history in Redis.
6. Data expires after one hour.
7. `session_id` and `reply` are returned.

---

## API Reference

### `POST /chat`

| Field | Type | Required | Description |
|---|---|---|---|
| `message` | string | Yes | Employee's question |
| `session_id` | string | No | Send to continue an existing session |

Response:

```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "reply": "To request annual leave, ..."
}
```

### `GET /history/{session_id}`

```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "messages": [
    {"role": "user", "message": "How do I request annual leave?"},
    {"role": "assistant", "message": "To request annual leave, ..."}
  ]
}
```

### PowerShell example

```powershell
$body = @{ message = "How do I request annual leave?" } | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:8000/chat -Method Post -Body $body -ContentType "application/json"
```

---

## Sample Questions

- How do I request annual leave?
- How many days of annual leave do I get?
- What is the difference between sick leave and casual leave?
- Can I carry forward unused leave?
- How much notice do I need to give before taking leave?
- Who approves my leave request?

Follow-up questions such as "What about sick leave?" work because the session keeps context.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Activate this project's `.venv` and run `python -m pip install -r requirements.txt` |
| `.env` not loaded | File must be named exactly `.env`, sit next to `main.py`, and have no quotes or extra spaces |
| Azure auth error | Run `az login`; choose the right subscription |
| `403` / access denied | Your account needs access to the Foundry project |
| Agent not found | Check endpoint and that `FOUNDRY_AGENT_NAME` matches exactly |
| Redis connection error (API) | Start Docker; `docker exec retail-redis redis-cli ping` should return `PONG` |
| History empty (API) | Session expired after 1 hour, or wrong `session_id` |
| Port 8000 in use (API) | `python -m uvicorn main:app --reload --port 8001` |

---

## What This Exercise Teaches

- Reusing one code pattern for a different agent just by changing configuration
- Building a CLI chatbot on a Foundry agent
- Converting it into a REST API with FastAPI
- Using Redis for short-term, expiring session memory
- Running supporting services with Docker
- Authenticating with Azure without storing keys

---

## Security Notes

- Never commit `.env` or `.venv`; list them in `.gitignore`.
- Leave answers can include company policy – keep endpoints private.
- Redis is bound to `127.0.0.1` for local use only.
- Add user authentication before exposing the API to employees.

---

## Possible Improvements

- Ground answers in the company's actual leave policy documents
- Add a tool that checks an employee's remaining leave balance
- Let employees submit a leave request through the agent
- Build a simple chat frontend
- Stream responses
- Add logging and monitoring
- Run the API and Redis together with Docker Compose
