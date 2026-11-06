# Restaurant AI Assistant

A command-line restaurant assistant built with LangChain and LangGraph. It uses a chat model through OpenRouter (or OpenAI as a fallback), searches the local `restaurants.json` data, and estimates dining costs.

## Features

- Search restaurants by name or cuisine.
- Calculate estimated dining costs for 1–20 guests.
- Keep conversation history during a session and start a fresh conversation with `/new`.
- Apply input validation and a restaurant-topic filter.
- Redact detected email addresses and phone numbers in displayed assistant replies, tool results, and tool arguments.
- Refuse reservation booking and payment requests.

Restaurant names, cuisine, prices, and seat availability come from `restaurants.json`. The assistant does not make bookings or process payments.

## Requirements

- Python 3.10 or later
- An OpenRouter API key, or an OpenAI API key
- A model/provider that supports tool calling

The default OpenRouter model is `openrouter/free`. Free model availability, rate limits, and tool-calling support can vary. You can set `OPENROUTER_MODEL` to another model available to your OpenRouter account.

## Setup on Windows

Open PowerShell in the project directory and create a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in the project directory:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=openrouter/free
```

Get an API key from [OpenRouter](https://openrouter.ai/keys). Keep the key private: do not commit `.env` or paste the key into source code.

To use OpenAI instead, omit `OPENROUTER_API_KEY` and configure:

```dotenv
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
```

When both provider keys are set, the app uses OpenRouter.

## Run

```powershell
python agent.py
```

Example:

```text
Welcome to the Restaurant Assistant!

you: Find Italian restaurants
Agent: ...
```

Enter `exit` or `quit` to end the application. Enter `/new` to clear the current conversation and begin a new one.

## Project files

| File | Purpose |
|---|---|
| `agent.py` | Loads provider settings, creates the LangChain agent, and runs the interactive chat loop. |
| `tools.py` | Defines restaurant search and dining-cost calculation tools. |
| `guardrails.py` | Validates input, filters topics, supports short contextual replies, and redacts detected PII for display. |
| `restaurants.json` | Local restaurant data used by the tools. |
| `requirements.txt` | Python package dependencies. |
| `.env` | Local API-key and model configuration; do not commit this file. |

## Guardrails

- Empty questions and questions longer than 1,000 characters are rejected.
- Questions are checked for restaurant-related keywords. Short replies such as “yes,” “no,” and “6 people” are accepted after an in-scope question in the current conversation.
- The dining-cost tool only accepts guest counts from 1 through 20.
- Email addresses and phone-number-like strings are masked in output printed by the application. This is display-time redaction, not a guarantee that such information is removed from messages sent to the model or provider.
- The assistant is instructed not to handle bookings or payments.

The restaurant-topic check is a lightweight keyword filter, not a comprehensive semantic safety system. The model still receives accepted user messages to answer them.
