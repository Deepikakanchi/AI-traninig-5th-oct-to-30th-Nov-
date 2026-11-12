# Vendor Purchase Approval Workflow

This project demonstrates a multi-agent procurement review flow. The Procurement Agent reviews the business justification, the Risk Agent assesses vendor risk, and an approval gateway automatically approves eligible requests or pauses for a manager decision. A Summary Agent prints the final demo record.

## Files

- `workflow.py` - application entry point and workflow graph
- `purchases.json` - sample purchase requests
- `requirements.txt` - Python dependencies
- `.env` - local Azure OpenAI configuration; keep this file private

## Requirements

- Python 3.14
- An Azure OpenAI / Azure AI Foundry endpoint with a deployed chat model
- An API key with access to that deployment

## Setup on Windows PowerShell

From this project folder:

```powershell
cd "C:\Users\Trainer\Downloads\AI TRAINIG\Day27\vendor_approval_workflow"
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

## Configure Azure OpenAI

Create or update `.env` in this folder:

```dotenv
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_BASE_URL=https://<your-resource>.openai.azure.com/openai/v1
AZURE_OPENAI_MODEL=<your-deployment-name>
```

Use your actual endpoint and deployment name. Do not commit `.env` or paste API keys into source control.

## Run

```powershell
python workflow.py
```

Requests that meet the workflow's approval rules are handled automatically. For other requests, the terminal prompts the manager to type `approve` or `reject`. This is a demonstration: it does not place an actual purchase order.

