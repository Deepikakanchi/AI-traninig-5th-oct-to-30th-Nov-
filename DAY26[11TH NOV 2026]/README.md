# Day 26 – Azure AI Foundry Agents (11 Nov 2026)

Part of the **AI Training Program (5 Oct – 30 Nov 2026)**.

Day 26 is about building with **Microsoft Foundry (Azure AI Foundry) agents** using the Azure Python SDK. The work grows in three steps: chatting with an agent from the terminal, exposing an agent as a REST API with Redis memory, and then applying the same pattern to a new use case (an employee leave assistant).

## Folder Structure

```text
DAY26[11TH NOV 2026]/
├── AZURE AGENT/                    # Step 1 – CLI chatbot + Foundry portal screenshots
│   ├── main.py
│   ├── requirements.txt
│   ├── README.md
│   └── *.png                       # agent setup, tools, evaluation, traces
├── Agent+api+redis_memory/         # Step 2 – Retail Support Agent as FastAPI + Redis
├── AI_agent_api_redis_exercise/    # Step 3 – Employee Leave Agent (CLI + FastAPI + Redis)
└── MAIN.txt
```

Each sub-folder has its own `README.md` with full setup details.

## Projects

### 1. AZURE AGENT – Foundry Agent CLI

A lightweight command-line chatbot that connects to an existing Foundry project and talks to a configured agent (default: `RetailSupportAgent`).

- Loads settings from `.env`
- Authenticates with `DefaultAzureCredential`
- Connects using `AIProjectClient` and opens a conversation
- Sends prompts in a loop until the user types `exit`

The folder also contains screenshots from the Foundry portal documenting the agent:

| Screenshot | What it shows |
|---|---|
| `agent_1.png` | The created agent |
| `agent instructions and tools.png` | Agent instructions and tool configuration |
| `agent tools and upload files .png` | Tools and uploaded knowledge files |
| `agent trace and insights.png` | Tracing and insights for agent runs |
| `agent evaluation .png`, `agent_evaluation_one.png` | Evaluation runs |
| `agent_evaluation_metrics.png` | Evaluation metrics |

### 2. Agent+api+redis_memory – Retail Support Agent API

Turns the retail agent into a **FastAPI** service with **Redis**-backed session memory.

- `POST /chat` – send a message; optional `session_id` continues a conversation
- `GET /history/{session_id}` – retrieve the stored chat history
- Conversation IDs and history are kept in Redis for 1 hour
- Request validation with Pydantic

### 3. AI_agent_api_redis_exercise – Employee Leave Support Agent

An extended exercise that applies the same pattern to a new agent, `EmployeeLeaveAgent`, which answers employee leave questions. It includes:

- **CLI version** – interactive terminal chat (no API, no Redis)
- **API version** – FastAPI + Redis with the same `/chat` and `/history/{session_id}` endpoints, interactive docs at `/docs`

## Tech Stack

| Area | Tools |
|---|---|
| Language | Python 3.14 (recommended) |
| AI platform | Microsoft Foundry (Azure AI Foundry) agents |
| SDK | `azure-ai-projects`, `azure-identity` |
| API | FastAPI, Uvicorn, Pydantic |
| Memory | Redis (via Docker) |
| Config | `python-dotenv` |

## Common Prerequisites

- Windows with PowerShell
- Python 3.14 (Python 3.16 may not install dependencies cleanly)
- Azure CLI, signed in with `az login`
- Access to a Microsoft Foundry project containing the agent
- Docker Desktop (for the Redis-based projects)

## Quick Start

Run these from inside the sub-project folder you want to try.

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
az login
```

Create a `.env` file:

```dotenv
FOUNDRY_PROJECT_ENDPOINT=<your Microsoft Foundry project endpoint>
FOUNDRY_AGENT_NAME=<RetailSupportAgent or EmployeeLeaveAgent>
REDIS_URL=redis://localhost:6379/0   # API projects only
```

**CLI projects:**

```powershell
python main.py
```

**API projects** – start Redis, then the server:

```powershell
docker run -d --name retail-redis -p 127.0.0.1:6379:6379 redis:7-alpine
docker exec retail-redis redis-cli ping   # should print PONG
python -m uvicorn main:app --reload
```

Then open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to test the endpoints.

## Example API Call

```json
POST /chat
{
  "message": "How do I request annual leave?"
}
```

```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "reply": "To request annual leave, ..."
}
```

Send the returned `session_id` with your next message to continue the same conversation.

## Troubleshooting

- **Package not found** – activate `.venv` and reinstall from `requirements.txt`.
- **Azure auth error / 403** – run `az login` and check your account has access to the Foundry project.
- **Agent not found** – confirm `FOUNDRY_AGENT_NAME` matches the agent name in the portal exactly.
- **Redis connection error** – make sure Docker is running and `redis-cli ping` returns `PONG`.
- **Port 8000 in use** – run Uvicorn with `--port 8001`.

## Key Learnings

- Connecting to Foundry agents from Python with `AIProjectClient` and `DefaultAzureCredential`
- Keeping multi-turn context with Foundry conversations
- Wrapping an agent in a REST API with FastAPI
- Using Redis as short-term session memory with expiry
- Configuring, tracing and evaluating agents in the Foundry portal

## Security Note

Never commit `.env` files, endpoints or credentials. Keep `.env` listed in `.gitignore`.
