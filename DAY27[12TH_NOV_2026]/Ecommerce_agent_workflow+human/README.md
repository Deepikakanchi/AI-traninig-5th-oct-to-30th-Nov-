# E-commerce Returns Review Workflow

This project reviews customer refund and replacement requests using Microsoft Agent Framework. It combines AI agent assessments with deterministic Python policy checks and routes requests that fail any automatic-approval condition to a manager.

## Files

- `workflow.py` - application entry point, policy checks, agents, and approval workflow
- `returns.json` - the 10 sample customer return requests loaded by the application
- `requirements.txt` - Python dependencies
- `.env` - optional Azure OpenAI configuration; keep this file private
- `purchases.json` - not used by this returns project; it belongs to the separate purchase-request example

## Automatic-approval policy

A request is automatically approved only if all of these conditions pass:

1. The amount is below INR 25,000.
2. The request is within 30 days of delivery.
3. An invoice is available.
4. The item is unopened, or it is damaged and photo evidence is available.
5. The customer has fewer than three previous returns in the last 90 days.
6. The risk assessment is not HIGH.

Any failed condition requires human review. The manager must enter `approve` or `reject`. A human rejection is preserved as the final decision.

## Requirements

- Python 3.14
- For AI-powered agent assessments: an Azure OpenAI / Azure AI Foundry endpoint, deployment, and API key

## Setup on Windows PowerShell

From this project folder:

```powershell
cd "C:\Users\Trainer\Downloads\AI TRAINIG\Day27\Ecommerce_agent_assignment"
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell prevents environment activation, run this in the current terminal and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Configure Azure OpenAI (optional)

To enable AI agent assessments, create or update `.env` in this folder:

```dotenv
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_BASE_URL=https://<your-resource>.openai.azure.com/openai/v1
AZURE_OPENAI_MODEL=<your-deployment-name>
```

Without these settings, the application uses deterministic policy checks and still prompts a manager for requests requiring review. Do not commit `.env` or paste API keys into source control.

## Run

```powershell
python workflow.py
```

Each request produces a structured output with the request and order IDs, product and amount, eligibility findings, risk assessment, approval route, final decision, and customer communication draft. This is a simulation only: no payments are processed, no messages are sent, and no product replacements are initiated. When Azure settings are provided, agent calls may incur Azure usage charges.

