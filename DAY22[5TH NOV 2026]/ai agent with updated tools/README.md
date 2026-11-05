# LangChain Workshop AI Agent

A small LangChain-based conversational assistant for searching available training workshops and calculating their total fees.

## Overview

This project demonstrates a simple AI agent built with:

- LangChain
- LangGraph
- OpenAI model integration
- Custom tools for workshop lookup and fee calculation
- PII input detection and an output-sanitization helper

The assistant can:

- Search workshops by title
- Return workshop details such as ID, duration, and fee
- List all available workshops
- Find the workshop with the lowest listed fee
- Calculate the cost for one workshop and a participant count
- Apply a coupon code to a fee and report the discount and final fee
- Reject unrelated questions and keep answers focused on workshops

## Project Structure

```text
.
├── agent.py              # Main agent entry point and CLI loop
├── tools.py              # Workshop search and fee calculation tools
├── guardrails.py         # PII detection and output-sanitization helper
├── workshops.json        # Workshop catalog data
├── coupons.json          # Coupon codes and discount rates
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

### 2. Workshop listing and fee calculation
The `list_all_workshops` tool returns the workshop catalog, and
`find_cheapest_workshop` returns the workshop with the lowest listed fee.

The `calculate_workshop_fee` tool calculates the cost for one workshop using:

- workshop ID
- number of participants

Example:

- Workshop: `W101`
- Participants: `2`
- Total fee: `6000`

Participant counts must be between 1 and 30. The current fee-calculation tool
accepts one workshop ID per call; it does not calculate a combined total for
multiple workshops.

### 3. Coupon codes
Coupon codes and their discount rates are stored in `coupons.json`. The
`apply_coupon_code` tool applies a valid coupon to the fee amount passed to it.
Coupon matching is case-insensitive.

Available example codes:

| Code | Discount |
|---|---:|
| `SAVE10` | 10% |
| `WELCOME15` | 15% |
| `DISCOUNT20` | 20% |

For example, `DISCOUNT20` applied to a fee of `6000` gives a discount of
`1200` and a final fee of `4800`. For multiple workshops, the current tool
does not calculate the combined fee; provide the correct total fee to the
coupon tool if applying a discount to multiple workshop costs.

### 4. Guardrails
The application includes safeguards to:

- detect PII in user input (email and phone numbers)
- stop the CLI when personal contact details are detected in user input

`guardrails.py` also defines a helper to redact email addresses and phone
numbers from text, but the current `agent.py` does not apply it to generated
answers.

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

You: Apply DISCOUNT20 to 12000
Agent: The discounted fee is 9600.
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
