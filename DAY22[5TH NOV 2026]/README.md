# AI Agent Projects

This repository contains four small AI assistant projects. Each one uses tools to work with local JSON data, so the model looks up real records instead of inventing details.

| # | Project | What it does | Stack | Model provider |
|---|---|---|---|---|
| 1 | [AI Library Assistant](#1-ai-library-assistant) | Search a book catalog and make reservations through a chat UI | React (Vite) + FastAPI | OpenRouter |
| 2 | [LangChain Workshop Agent (Guarded + Basic)](#2-langchain-workshop-agent-guarded--basic) | Search workshops and calculate fees from the command line | LangChain | OpenAI |
| 3 | [LangChain Workshop AI Agent (PII Guardrails)](#3-langchain-workshop-ai-agent-pii-guardrails) | Search workshops, calculate fees, and filter personal data | LangChain + LangGraph | OpenAI |
| 4 | [LangChain Workshop AI Agent (Coupons)](#4-langchain-workshop-ai-agent-coupons) | Search and list workshops, find the cheapest, calculate fees, and apply coupon codes | LangChain + LangGraph | OpenAI |

> Folder names below are placeholders. Replace them with the actual folder names in your repository.

## Repository structure

```text
.
├── library-ai-assistant/          # Project 1
│   ├── frontend--/                # React chat interface
│   └── Library_AI_Agent/
│       └── Library_AI_Agent/      # FastAPI backend
├── workshop-agent/                # Project 2
├── workshop-agent-guardrails/     # Project 3
└── workshop-agent-coupons/        # Project 4
```

## Common requirements

- Python 3.10 or later (all projects)
- Node.js and npm (Project 1 only)
- An OpenRouter API key (Project 1) or an OpenAI API key (Projects 2 and 3)

Every project reads its API key from a local `.env` file. Keep `.env` files private and never commit them.

---

## 1. AI Library Assistant

A full-stack library assistant with a React chat interface and a Python API. Users can search for books and request a reservation, which must be confirmed before it is saved.

### Features

- Search the catalog by title, author, or category.
- Chat with an AI assistant powered by a model available through OpenRouter.
- Review, confirm, or cancel a reservation before it is finalized.
- Store the catalog (`books.json`) and reservations (`reservations.json`) as local JSON files.

### Key files

| File | Purpose |
|---|---|
| `frontend--/src/` | React application |
| `Library_AI_Agent/Library_AI_Agent/api.py` | FastAPI endpoints |
| `Library_AI_Agent/Library_AI_Agent/agent.py` | Command-line agent |
| `Library_AI_Agent/Library_AI_Agent/tools.py` | Catalog search and reservation logic |
| `books.json` / `reservations.json` | Book catalog and reservation records |

### Setup

**Backend**

```powershell
cd .\Library_AI_Agent\Library_AI_Agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt fastapi uvicorn pydantic
```

Create `.env` in the same folder:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=your_openrouter_model
```

Start the API:

```powershell
python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

API docs are available at `http://127.0.0.1:8000/docs`.

**Frontend** (in a second terminal)

```powershell
cd .\frontend--
npm install
npm run dev
```

Open the URL printed by Vite (usually `http://localhost:5173`). To point the frontend at a different backend, set `VITE_API_URL` in `frontend--\.env` and restart Vite.

### API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Check that the API is running |
| `POST` | `/chat` | Send a message and receive a response |
| `POST` | `/confirm-reservation` | Confirm or cancel a pending reservation |

### Notes

- A confirmed reservation is appended to `reservations.json` and reduces the book's `available_copies`. Back up the JSON files before resetting sample data.
- If the backend exits on startup, check that both `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` are set.

---

## 2. LangChain Workshop Agent (Guarded + Basic)

A command-line workshop enquiry assistant built with LangChain. It searches a local workshop catalog and calculates fees in INR using tools.

### Modes

- **Guarded assistant** (`agent_guarded.py`): restricts requests to workshop topics and requires tool evidence for details and fees. Recommended for normal use.
- **Basic assistant** (`agent.py`): a minimal tool-calling example with conversation memory.

Neither mode can book workshops or accept payments.

### Key files

| File | Purpose |
|---|---|
| `agent_guarded.py` | Workshop-only assistant with input/output guardrails |
| `agent.py` | Basic tool-calling assistant |
| `tools.py` | Catalog search and fee-calculation tools |
| `workshops.json` | Workshop catalog |
| `test_tools.py` | Local tool tests (no API calls) |
| `.env.example` | Template for environment settings |

### Setup and run

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Set your key in `.env` (`OPENAI_MODEL` is optional and defaults to `gpt-4o-mini`):

```dotenv
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
```

```powershell
python agent_guarded.py   # or: python agent.py
python test_tools.py      # run tool tests without an API key
```

### Workshop catalog

| ID | Workshop | Duration | Mode | Fee per person |
|---|---|---:|---|---:|
| W101 | Python Automation Essentials | 2 days | Online | INR 3,000 |
| W102 | Generative AI Fundamentals | 1 day | Online | INR 4,000 |
| W103 | Power BI Dashboards | 2 days | Classroom | INR 3,500 |
| W104 | Azure AI Basics | 2 days | Online | INR 4,500 |

Fee calculations support 1–100 participants.

---

## 3. LangChain Workshop AI Agent (PII Guardrails)

A lightweight conversational assistant built with LangChain and LangGraph. It searches workshops, calculates total fees, and protects personal contact details.

### Features

- **Workshop search:** the `search_workshops` tool finds workshops by keyword.
- **Fee calculation:** the `calculate_workshop_fee` tool multiplies the fee by the participant count (for example, W101 × 4 participants = 12000).
- **Guardrails:** detects email addresses and phone numbers in user input, blocks the conversation when they are shared, and redacts them from generated output.
- **Scope control:** rejects questions unrelated to workshops.

### Key files

| File | Purpose |
|---|---|
| `agent.py` | Main agent and CLI loop |
| `tools.py` | Workshop search and fee calculation |
| `guardrails.py` | PII detection and output sanitization |
| `workshops.json` | Workshop catalog |
| `requirements.txt` | `langchain`, `langchain-openai`, `langgraph`, `python-dotenv` |

### Setup and run

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

Create `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

```bash
python agent.py
```

---

## 4. LangChain Workshop AI Agent (Coupons)

An extended version of the Project 3 agent, built with LangChain and LangGraph. Along with workshop search and fee calculation, it can list the full catalog, find the cheapest workshop, and apply coupon codes.

### Features

- **Workshop search:** `search_workshops` finds workshops by keyword.
- **Catalog listing:** `list_all_workshops` returns every workshop in the catalog.
- **Cheapest workshop:** `find_cheapest_workshop` returns the workshop with the lowest listed fee.
- **Fee calculation:** `calculate_workshop_fee` calculates the cost for one workshop and a participant count of 1–30 (for example, W101 × 2 participants = 6000). It handles one workshop per call and does not total multiple workshops.
- **Coupon codes:** `apply_coupon_code` applies a valid coupon from `coupons.json` to the fee passed to it and reports the discount and final fee. Codes are case-insensitive.
- **Guardrails:** detects email addresses and phone numbers in user input and stops the CLI when they are found. `guardrails.py` also includes a redaction helper, but `agent.py` does not currently apply it to generated answers.
- **Scope control:** rejects questions unrelated to workshops.

### Coupon codes

| Code | Discount |
|---|---:|
| `SAVE10` | 10% |
| `WELCOME15` | 15% |
| `DISCOUNT20` | 20% |

Example: `DISCOUNT20` applied to 6000 gives a discount of 1200 and a final fee of 4800. To discount several workshops together, pass their combined total to the coupon tool.

### Key files

| File | Purpose |
|---|---|
| `agent.py` | Main agent and CLI loop |
| `tools.py` | Search, listing, fee calculation, and coupon tools |
| `guardrails.py` | PII detection and output-sanitization helper |
| `workshops.json` | Workshop catalog |
| `coupons.json` | Coupon codes and discount rates |
| `requirements.txt` | `langchain`, `langchain-openai`, `langgraph`, `python-dotenv` |

### Setup and run

Setup is the same as Project 3: create a virtual environment, run `pip install -r requirements.txt`, and add `OPENAI_API_KEY` and `OPENAI_MODEL` to a `.env` file. Then run:

```bash
python agent.py
```

### Example usage

```text
You: I want to enroll in W101 for 4 people
Agent: Total fee for Python Fundamentals for 4 participants is 12000.

You: Apply DISCOUNT20 to 12000
Agent: The discounted fee is 9600.
```

---

## CLI commands (Projects 2, 3, and 4)

| Command | Action |
|---|---|
| `/new` | Start a new conversation |
| `exit` | Quit the application |

Conversation memory lasts only while the program is running.

## How the workshop agents differ

| | Project 2 | Project 3 | Project 4 |
|---|---|---|---|
| Framework | LangChain | LangChain + LangGraph | LangChain + LangGraph |
| Guardrail focus | Topic restriction and tool evidence | PII detection and redaction | PII detection in input (redaction helper not applied) |
| Entry points | `agent_guarded.py`, `agent.py` | `agent.py` | `agent.py` |
| Extra tools | — | — | List all, find cheapest, apply coupon |
| Participant limit | 1–100 | Not stated | 1–30 |
| Local tests | `test_tools.py` | Not included | Not included |
| Catalog | Includes delivery mode (online/classroom) | ID, title, duration, fee | ID, title, duration, fee, plus `coupons.json` |

## License

These projects are provided for educational and demonstration purposes.
