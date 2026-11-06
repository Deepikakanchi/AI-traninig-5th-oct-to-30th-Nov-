# Day 24 (6th Nov 2026): Restaurant AI Agent and AI Agents Study Guide

This folder contains two items from Day 24 of the AI training: a working restaurant assistant built with LangChain and LangGraph, and a study guide assignment on LangGraph, the agent lifecycle, and multi-agent coordination.

| # | Folder | Project | What it is | Stack |
|---|---|---|---|---|
| 1 | [`Restaurant_AI_Agent`](./Restaurant_AI_Agent/) | [Restaurant AI Assistant](#1-restaurant-ai-assistant) | Command-line assistant that searches restaurants and estimates dining costs | LangChain + LangGraph, OpenRouter or OpenAI |
| 2 | [`ai agent assignment`](./ai%20agent%20assignment/) | [AI Agents Study Guide](#2-ai-agents-study-guide-assignment) | 13-page PDF guide on LangGraph, agent lifecycle, and multi-agent patterns | Python, ReportLab, Matplotlib |

## Folder structure

```text
DAY24[6TH NOV 2026]/
├── Restaurant_AI_Agent/        # Project 1: Restaurant AI Assistant
│   ├── agent.py
│   ├── tools.py
│   ├── guardrails.py
│   ├── restaurants.json
│   └── requirements.txt
├── ai agent assignment/        # Project 2: Study guide assignment
│   ├── LangGraph_Agents_Guide.pdf
│   └── README.md
├── MAIN.txt                    # Day 24 work files
└── README.md                   # This file
```

Because `ai agent assignment` contains spaces, wrap it in quotes when using `cd`:

```powershell
cd "ai agent assignment"
```

---

## 1. Restaurant AI Assistant

**Folder:** `Restaurant_AI_Agent`

A command-line restaurant assistant built with LangChain and LangGraph. It uses a chat model through OpenRouter (with OpenAI as a fallback), searches local restaurant data, and estimates dining costs. It does not make bookings or process payments.

### Features

- Search restaurants by name or cuisine.
- Estimate dining costs for 1–20 guests.
- Keep conversation history during a session; start fresh with `/new`.
- Validate input and filter out questions that aren't about restaurants.
- Mask email addresses and phone numbers in displayed replies, tool results, and tool arguments.
- Refuse reservation and payment requests.

Restaurant names, cuisine, prices, and seat availability all come from `restaurants.json`.

### Key files

| File | Purpose |
|---|---|
| `agent.py` | Loads provider settings, creates the agent, and runs the chat loop |
| `tools.py` | Restaurant search and dining-cost calculation tools |
| `guardrails.py` | Input validation, topic filter, short-reply handling, and PII redaction for display |
| `restaurants.json` | Local restaurant data |
| `requirements.txt` | Python dependencies |
| `.env` | API key and model settings (do not commit) |

### Requirements

- Python 3.10 or later
- An OpenRouter API key or an OpenAI API key
- A model that supports tool calling

### Setup (Windows)

```powershell
cd .\Restaurant_AI_Agent
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in `Restaurant_AI_Agent`:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=openrouter/free
```

Get a key from [OpenRouter](https://openrouter.ai/keys). The default model, `openrouter/free`, may vary in availability, rate limits, and tool-calling support, so you can set `OPENROUTER_MODEL` to another model on your account.

To use OpenAI instead, leave out `OPENROUTER_API_KEY` and set:

```dotenv
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
```

If both keys are set, the app uses OpenRouter.

### Run

```powershell
python agent.py
```

```text
Welcome to the Restaurant Assistant!

you: Find Italian restaurants
Agent: ...
```

| Command | Action |
|---|---|
| `/new` | Clear the conversation and start a new one |
| `exit` or `quit` | Close the application |

### Guardrails

- Empty questions and questions over 1,000 characters are rejected.
- Questions must contain restaurant-related keywords. Short follow-ups such as "yes", "no", or "6 people" are accepted after an in-scope question.
- The dining-cost tool only accepts 1–20 guests.
- Emails and phone numbers are masked in printed output only. They are not removed from messages sent to the model provider.
- The assistant is instructed not to handle bookings or payments.

The topic check is a lightweight keyword filter, not a full safety system.

---

## 2. AI Agents Study Guide (Assignment)

**Folder:** `ai agent assignment`

A 13-page PDF study guide, `LangGraph_Agents_Guide.pdf`, with diagrams, code examples, and tables. Open it in any PDF reader and read it in order, since each part builds on the one before.

### Topics covered

1. **LangGraph and LangChain:** LangChain provides the building blocks (models, prompts, tools, retrievers), and LangGraph connects them into a workflow using state, nodes, and edges. Includes a code example and a "when to use which" table.
2. **Agent lifecycle:** the run-time loop (receive goal, plan, choose tool, execute, observe, update memory, decide if done), why agents fail and how to fix it, and the development stages from define through monitor and improve.
3. **Multi-agent coordination patterns:** supervisor, network (swarm), and hierarchical teams, with a comparison table and advice on when one agent is enough.

The final section ties all three together with a worked example, common mistakes, a learning path, and a glossary.

### Diagrams

- LangChain and LangGraph stack
- Tool-calling agent as a graph
- Agent loop
- The three multi-agent patterns

### Notes

- **"MCP":** The original slide uses MCP for "Multi-agent coordination patterns". In AI, MCP usually means Model Context Protocol. The PDF explains the difference.
- **Code examples:** LangChain and LangGraph change quickly, so check the official docs before running any code.
- **Authorship:** The guide's text was generated with AI. If the assignment must be your own work, use it as study material and rewrite it in your own words.

---

## License

These projects are provided for educational and demonstration purposes.
