# Workshop AI Agent

This project is a small multi-agent Python app for finding training workshops, estimating group fees, and recommending the best option based on the user's topic and budget.

## What it does

The app uses an agent workflow with three specialized roles:

- SearchAgent: looks up workshop matches by topic/title
- PricingAgent: calculates the total group cost for a selected workshop
- RecommendationAgent: recommends the most suitable workshop using verified search and pricing results

It reads workshop data from `workshops.json` and applies the logic through tools defined in `tools.py`.

## Project structure

- `agent.py` - defines the agents and their responsibilities
- `sequential.py` - runs the sequential multi-agent workflow
- `tools.py` - workshop search and fee calculation tools
- `workshops.json` - sample workshop catalog
- `requirements.txt` - Python dependencies

## Requirements

- Python 3.10+
- OpenAI API access with a valid API key

## Setup

1. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure your environment variables. The project loads values from a `.env` file automatically.

   Example `.env`:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_CHAT_MODEL=gpt-4o-mini
   ```

## Run the app

```bash
python sequential.py
```

Then enter a prompt such as:

- "Find Python workshops under 20000 INR for 10 participants"
- "Suggest a workshop on Azure for 5 people"
- "Which Python course is best for a group of 8 within my budget?"

## Example workshop data

The app currently includes sample workshops such as:

- W101: Python Fundamentals
- W102: Advanced Python
- W103: Azure Fundamentals
- W104: Power BI Essentials

## Notes

- The tool validation ensures participant counts are between 1 and 30.
- The app uses the `agent_framework` library and a sequential orchestration pattern.
- The workshop fee is reported in INR.
