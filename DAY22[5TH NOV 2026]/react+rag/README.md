# LangChain Workshop Agent

A command-line workshop enquiry assistant built with LangChain. It searches a local JSON catalog and calculates workshop fees in INR using tools, rather than relying on the model to invent workshop details or prices.

The project includes two modes:

- **Guarded assistant** (`agent_guarded.py`): restricts requests to workshop-related topics and requires tool evidence for workshop details and fees. Recommended for normal use.
- **Basic assistant** (`agent.py`): a minimal tool-calling example with conversation memory.

Neither mode can book workshops or accept payments.

## Requirements

- Python 3.10 or later
- An OpenAI API key to run either assistant

## Setup

Open PowerShell in the project directory and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set your OpenAI API key:

```dotenv
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
```

`OPENAI_MODEL` is optional; if omitted, the assistant uses `gpt-4o-mini`. Keep `.env` private and do not commit your API key.

## Run

Start the guarded assistant:

```powershell
python agent_guarded.py
```

Or start the basic assistant:

```powershell
python agent.py
```

Example questions:

- `Show me Python workshops`
- `How much would W101 cost for 4 participants?`
- If the assistant asks for a participant count, reply with a number such as `4`.

Enter `/new` to start a fresh conversation or `exit` to quit. Conversation memory is held in memory while the program runs; it is not saved between runs.

## Workshop catalog

The assistant reads workshop data from [`workshops.json`](./workshops.json).

| ID | Workshop | Duration | Mode | Fee per person |
|---|---|---:|---|---:|
| W101 | Python Automation Essentials | 2 days | Online | INR 3,000 |
| W102 | Generative AI Fundamentals | 1 day | Online | INR 4,000 |
| W103 | Power BI Dashboards | 2 days | Classroom | INR 3,500 |
| W104 | Azure AI Basics | 2 days | Online | INR 4,500 |

Fee calculations support 1–100 participants. Update the JSON catalog to change workshop details or prices.

## Run local tool tests

The tool tests do not make OpenAI API calls and can be run before configuring an API key:

```powershell
python test_tools.py
```

The tests cover catalog search, a fee calculation, an unknown workshop ID, and an invalid participant count.

## Project files

- [`agent_guarded.py`](./agent_guarded.py) — workshop-only assistant with input/output guardrails.
- [`agent.py`](./agent.py) — basic LangChain tool-calling assistant.
- [`tools.py`](./tools.py) — catalog search and fee-calculation tools.
- [`workshops.json`](./workshops.json) — workshop catalog data.
- [`test_tools.py`](./test_tools.py) — local tests for the tools.
- [`requirements.txt`](./requirements.txt) — Python dependencies.
- [`.env.example`](./.env.example) — template for local environment settings.
