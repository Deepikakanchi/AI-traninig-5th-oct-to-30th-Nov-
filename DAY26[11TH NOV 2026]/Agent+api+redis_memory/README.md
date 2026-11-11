# Azure Retail Support Agent API

This project is a Python FastAPI service that connects to an Azure AI Foundry project and exposes a conversational agent as a REST API. It is designed for retail support use cases where a business wants a lightweight AI assistant to answer product and customer-support style questions while keeping session-based chat history in Redis.

The service authenticates to Azure using `DefaultAzureCredential`, connects to an existing AI Foundry project, and interacts with a configured agent such as `RetailSupportAgent`.

## Overview

The application includes:

- a FastAPI API with a `/chat` endpoint for sending messages
- a `/history/{session_id}` endpoint for retrieving prior messages
- Redis-backed session conversation storage and message history
- Azure AI Foundry integration using the Azure Python SDK
- a configurable environment-based setup for project endpoint and agent name

This project is useful as a small, self-contained backend component for testing or integrating an AI-powered retail assistant into a wider application.

## Project Purpose

The API is tailored for a retail support workflow in which:

- a user sends a question to the assistant
- the assistant continues the same conversation for that session
- the conversation is stored in Redis for a limited time
- the agent responds using the configured Azure AI Foundry model/agent

This is a practical solution for local development, demos, prototypes, or internal tooling that needs a simple conversational interface without a full production platform deployment.

## Features

- FastAPI-based HTTP API
- Session-aware messaging with Redis
- Persistent chat history per session for 1 hour by default
- Azure identity authentication via `DefaultAzureCredential`
- Integration with an existing Azure AI Foundry project and deployed agent
- Validation for request payloads using Pydantic
- Minimal configuration with `.env` support

## Project Structure

```text
azure_agent/
├── main.py
├── requirements.txt
├── .env                 # local environment file (not usually committed)
├── .venv                # local virtual environment
├── __pycache__          # Python cache files
├── README.md
└── .gitignore           # optional, if added locally
```

## Prerequisites

Before running this project, ensure you have:

- Python 3.9 or later
- An Azure subscription
- Access to an Azure AI Foundry project
- A deployed or configured AI agent in that project
- Azure CLI installed and logged in (`az login`) or another supported `DefaultAzureCredential` source
- Redis running locally or reachable through a Redis URL

## Required Azure and Runtime Setup

The app needs the following environment variables:

- `FOUNDRY_PROJECT_ENDPOINT`: the Azure AI Foundry project endpoint
- `FOUNDRY_AGENT_NAME`: the name of the agent to call (defaults to `RetailSupportAgent`)
- `REDIS_URL`: Redis connection string (defaults to `redis://localhost:6379/0`)

Example:

```env
FOUNDRY_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project
FOUNDRY_AGENT_NAME=RetailSupportAgent
REDIS_URL=redis://localhost:6379/0
```

## Installation

1. Open a terminal in the project folder.
2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate it:

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

macOS/Linux:

```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running Redis

This project uses Redis to store conversation IDs and chat history.

If Redis is installed locally, start it with the default service or via Docker:

```bash
docker run --name redis-retail-agent -p 6379:6379 -d redis
```

## Running the API

From the project root, start the server with:

```bash
uvicorn main:app --reload
```

The application will be available at:

- `http://127.0.0.1:8000`

## API Endpoints

### 1. Chat with the agent

Endpoint:

```http
POST /chat
```

Request body:

```json
{
  "message": "What products are best for a small online store?",
  "session_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

Fields:

- `message`: required user message
- `session_id`: optional UUID; if not provided, a new one is generated automatically

Example response:

```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "reply": "Here are a few good options for a small online store..."
}
```

### 2. Get session history

Endpoint:

```http
GET /history/{session_id}
```

Example:

```http
GET /history/123e4567-e89b-12d3-a456-426614174000
```

Example response:

```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "messages": [
    {"role": "user", "message": "What products are best for a small online store?"},
    {"role": "assistant", "message": "Here are a few good options for a small online store..."}
  ]
}
```

## Application Flow

The service works as follows:

1. It loads environment variables from `.env`.
2. It creates a Redis connection.
3. It connects to the Azure AI Foundry project using `AIProjectClient`.
4. It retrieves the configured agent using `project.get_openai_client()`.
5. When a user sends a chat request:
   - a session ID is created or reused
   - Redis stores the conversation ID and history
   - the agent is called with the current message
   - the response is stored in Redis
   - the reply is returned to the caller

## How the Code Works

The main logic is in `main.py`.

Key components:

- `app = FastAPI(title="Retail Support Agent API")`
- `db = redis.Redis.from_url(...)`
- `AIProjectClient(...)` for Azure Foundry access
- `ChatRequest` model for validating incoming requests
- `/chat` route for processing conversations
- `/history/{session_id}` route for retrieving prior messages

## Authentication Model

The project uses `DefaultAzureCredential`, which allows Azure authentication through common sources such as:

- Azure CLI (`az login`)
- environment-based credentials
- managed identity
- Visual Studio / developer environment credentials

For local development, the most common path is:

```bash
az login
```

## Environment Example

Create a `.env` file like this:

```env
FOUNDRY_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project
FOUNDRY_AGENT_NAME=RetailSupportAgent
REDIS_URL=redis://localhost:6379/0
```

## Dependency Summary

The project dependencies are inside `requirements.txt`:

```txt
fastapi
uvicorn
redis
azure-ai-projects>=2.9.0
azure-identity
python-dotenv
```

These packages provide:

- API framework for the HTTP service
- local server runner
- Redis client for session management
- Azure AI Foundry client access
- Azure authentication
- `.env` file support

## Troubleshooting

### Missing environment variables

If `FOUNDRY_PROJECT_ENDPOINT` is missing, the app will fail before connecting to Azure.

Fix:

- create a `.env` file
- confirm the variable names match exactly
- restart the app after updating the file

### Redis connection errors

If Redis is not running or not reachable, requests will fail when trying to create or fetch conversation state.

Fix:

- ensure Redis is running
- check the `REDIS_URL`
- verify Redis is accepting connections on the configured port

### Azure authentication issues

If `DefaultAzureCredential` cannot authenticate:

```bash
az login
```

Then confirm that the signed-in identity has access to the Azure AI Foundry project.

### 403 or access denied

This usually means the current Azure user or managed identity does not have permission to the project.

Fix:

- verify the correct Azure account is active
- confirm access to the AI Foundry project
- validate that the endpoint is correct

### Agent not found

If the configured agent name does not exist in the Azure AI Foundry project, the request will fail.

Fix:

- verify `FOUNDRY_AGENT_NAME`
- check that the agent was created and deployed
- use the exact agent name configured in the Azure project

## Security Notes

- Do not commit `.env` files containing real Azure credentials.
- Keep Redis credentials and project endpoints in a secure secret store when used beyond local development.
- Prefer least-privilege access for Azure identities.
- Validate and limit input to prevent overly large messages.

## Example Use Cases

This project is appropriate for:

- testing a retail support agent locally
- creating a small proof-of-concept AI assistant
- connecting a conversational AI layer to a web app or internal tool
- validating Foundry agent behavior before integration into a larger platform

## Notes

This is a lightweight backend project intended for local experimentation and simple integration. It is intentionally compact and does not include a full production deployment pipeline, authentication layer for end users, database schema management, or multi-service architecture.

## Possible Improvements

Future enhancements could include:

- adding request logging and structured error handling
- supporting multi-agent selection
- adding conversation summaries or export features
- adding streaming responses
- adding a front-end interface or API gateway
- implementing production-grade monitoring and deployment configuration

## License

This project does not currently include a license file. If you plan to distribute or share the project publicly, add an appropriate license based on your organization or project requirements.
