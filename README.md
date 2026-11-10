# Customer Feedback Concurrent Agents

A Python example that analyzes customer feedback using three AI agents running concurrently. Each agent receives the same records from `feedback.json` and has a different task:

- **SentimentAgent** counts positive, neutral, and negative ratings and cites example feedback IDs.
- **IssueAgent** identifies the three most common complaints and cites supporting IDs.
- **ImprovementAgent** suggests three practical actions tied to feedback IDs.

This is a fixed analysis workflow, not an interactive question-and-answer chatbot. The agents use only the supplied feedback data.

## Requirements

- Python 3.10 or later
- An OpenRouter API key with sufficient credits for the selected model

## Setup on Windows

Open PowerShell in the project folder and create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

Create a `.env` file in the project folder with your OpenRouter key and model:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=openai/gpt-4.1-mini
```

Keep your real API key private. Do not commit the `.env` file or share its contents.

## Run

```powershell
python concurrent_agents.py
```

The script prints the feedback count, each agent's response, and the total elapsed time. It reads `feedback.json` from the same folder as the script.

## Feedback data

`feedback.json` must contain a non-empty JSON list. Each record includes:

```json
{
  "id": "F001",
  "rating": 5,
  "area": "Checkout",
  "comment": "Checkout was quick and the discount code worked on my first try."
}
```

Ratings are interpreted as positive (4–5), neutral (3), and negative (1–2).

## Troubleshooting

- **Missing `OPENROUTER_API_KEY`:** Add a non-empty `OPENROUTER_API_KEY` value to `.env`.
- **HTTP 402 / insufficient credits:** Add credits or choose a model affordable by your OpenRouter key. Each agent is configured with an output limit of 8,192 tokens, but the provider's credit limit still applies.
- **Invalid feedback JSON:** Check that `feedback.json` contains a non-empty JSON list with valid JSON syntax.
