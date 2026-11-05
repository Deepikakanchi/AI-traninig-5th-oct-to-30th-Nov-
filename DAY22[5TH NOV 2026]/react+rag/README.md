# AI Library Assistant

A full-stack library assistant with a React chat interface and a Python API. Ask the assistant to find books, or request a reservation and confirm it before it is saved.

## Features

- Search the library catalog by book title, author, or category.
- Chat with an AI assistant powered by a model available through OpenRouter.
- Review and confirm or cancel a reservation before it is finalized.
- Store the catalog and reservations locally as JSON files.

## Project structure

```text
frontend--/
  src/                         React application
  package.json                 Frontend scripts and dependencies
Library_AI_Agent/
  Library_AI_Agent/
    api.py                     FastAPI endpoints
    agent.py                   Command-line agent
    tools.py                   Catalog search and reservation logic
    books.json                 Book catalog
    reservations.json          Reservation records
    requirements.txt           Python package requirements
```

## Requirements

- Python 3.10 or later
- Node.js and npm
- An OpenRouter API key and a model identifier supported by your account

## Setup

Run the following commands from the project directory containing `frontend--` and `Library_AI_Agent`.

### 1. Configure and start the backend

```powershell
cd .\Library_AI_Agent\Library_AI_Agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt fastapi uvicorn pydantic
```

Create a `.env` file in `Library_AI_Agent\Library_AI_Agent` with your own OpenRouter credentials:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=your_openrouter_model
```

Start the API:

```powershell
python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

The API is available at `http://127.0.0.1:8000`. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

### 2. Start the frontend

In a second terminal, return to the project directory and run:

```powershell
cd .\frontend--
npm install
npm run dev
```

Open the local URL printed by Vite (usually `http://localhost:5173`).

The frontend uses `http://127.0.0.1:8000` by default. To use a different backend URL, create `frontend--\.env` and set:

```dotenv
VITE_API_URL=http://127.0.0.1:8000
```

Restart the Vite development server after changing frontend environment variables.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Check that the API is running |
| `POST` | `/chat` | Send a chat message and receive an assistant response |
| `POST` | `/confirm-reservation` | Confirm or cancel a pending reservation |

## Frontend scripts

Run these commands from `frontend--`:

```powershell
npm run dev      # Start the Vite development server
npm run build    # Create a production build in dist/
npm run preview  # Preview the production build locally
npm run lint     # Run Oxlint
```

## Data files

The catalog is stored in `Library_AI_Agent\Library_AI_Agent\books.json`, and completed reservations are stored in `reservations.json`. A successful reservation appends to the reservation file and decreases the corresponding book's `available_copies` value. Back up these files before editing or resetting the sample data.

## Troubleshooting

- **Backend exits during startup:** Check that the backend `.env` file contains both `OPENROUTER_API_KEY` and `OPENROUTER_MODEL`.
- **Frontend cannot reach the API:** Make sure the backend is running on port `8000`, or set `VITE_API_URL` to the correct API base URL.
- **Python import or server errors:** Activate the virtual environment and install the backend packages using the command in the setup section.
