# IT Incident Routing System

This project uses Microsoft Agent Framework and Azure OpenAI to classify IT incidents and route them to an escalation or resolution agent.

## Files

- `graph_workflow.py` - application entry point and graph workflow
- `incidents.json` - sample incidents to process
- `requirements.txt` - Python dependencies
- `.env` - local Azure OpenAI configuration; keep this file private

## Requirements

- Python 3.14
- An Azure OpenAI / Azure AI Foundry endpoint with a deployed chat model
- An API key with access to that deployment

## Setup on Windows PowerShell

From this project folder:

```powershell
cd "C:\Users\Trainer\Downloads\AI TRAINIG\Day27\model_agent"
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
python graph_workflow.py
```

The program reads incidents from `incidents.json`, classifies each incident, and prints an escalation plan or troubleshooting guidance. Each run may make Azure OpenAI API calls.

