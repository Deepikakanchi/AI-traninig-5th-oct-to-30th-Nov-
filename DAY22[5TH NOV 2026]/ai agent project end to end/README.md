# LangChain Workshop AI Agent

A small LangChain-based conversational assistant for searching available training workshops and calculating their total fees.

## Overview

This project demonstrates a simple AI agent built with:

- LangChain
- LangGraph
- OpenAI model integration
- Custom tools for workshop lookup and fee calculation
- Input/output guardrails for PII filtering

The assistant can:

- Search workshops by title
- Return workshop details such as ID, duration, and fee
- Calculate total cost for a selected workshop and participant count
- Reject unrelated questions and keep answers focused on workshops

## Project Structure

```text
.
├── agent.py              # Main agent entry point and CLI loop
├── tools.py              # Workshop search and fee calculation tools
├── guardrails.py         # PII detection and output sanitization
├── workshops.json        # Workshop catalog data
├── requirements.txt      # Python dependencies
├── .env                  # Local environment variables (not committed)
└── README.md             # Project documentation
```

## Workshop Data

The project stores workshop records in `workshops.json`.

Example entries:

```json
[
  {
    "id": "W101",
    "title": "Python Fundamentals",
    "duration": "2 Days",
    "fee": 3000
  }
]
```

## Features

### 1. Workshop search
The `search_workshops` tool searches the catalog based on a keyword.

Example:

- "Show me Python workshops"
- "Find Azure training"

### 2. Fee calculation
The `calculate_workshop_fee` tool calculates total cost using:

- workshop ID
- number of participants

Example:

- Workshop: `W101`
- Participants: `4`
- Total fee: `12000`

### 3. Guardrails
The application includes safeguards to:

- detect PII in user input (email and phone numbers)
- block the conversation when personal contact details are provided
- redact detected email/phone values from generated output

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your OpenAI credentials:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

## Run the app

```bash
python agent.py
```

You will see a simple command-line chat interface.

Available commands:

- `/new` — start a new conversation thread
- `exit` — quit the application

## Example Usage

```text
You: Show me workshops about Python
Agent: I found Python Fundamentals.

You: I want to enroll in W101 for 4 people
Agent: Total fee for Python Fundamentals for 4 participants is 12000.
```

## Notes

- The agent is intentionally scoped to workshop-related questions only.
- It uses the provided workshop catalog and never invents prices or titles.
- It is designed as a lightweight demo application rather than a production-grade business system.

## Requirements

See `requirements.txt` for the installed dependencies:

- `langchain`
- `langchain-openai`
- `langgraph`
- `python-dotenv`

## License

This project is provided for educational and demonstration purposes.
