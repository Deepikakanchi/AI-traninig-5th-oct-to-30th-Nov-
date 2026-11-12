# Day 27: Microsoft Agent Framework Projects

This folder contains three independent Python projects. Each project has its own input data, workflow, dependencies, and optional Azure OpenAI configuration.

| Project folder | What it does | Input data | Run command |
|---|---|---|---|
| `model_agent` | Routes IT incidents to escalation or resolution guidance | `incidents.json` | `python graph_workflow.py` |
| `vendor_approval_workflow` | Reviews company purchase requests and asks a manager to approve or reject when required | `purchases.json` | `python workflow.py` |
| `Ecommerce_agent_assignment` | Reviews customer refund/replacement requests and escalates policy exceptions to a manager | `returns.json` | `python workflow.py` |

> These are separate examples. The e-commerce returns project uses `returns.json`; it does not use the vendor project's `purchases.json`.

## Requirements

- Windows PowerShell
- Python 3.14
- Git is optional and only needed if you want to version or share the projects
- Azure OpenAI / Azure AI Foundry endpoint, model deployment, and API key for AI-powered workflows

Each project includes its own `requirements.txt`. Create and activate a virtual environment inside the project you intend to run. This keeps its packages separate from other projects.

If PowerShell blocks activation, allow it for the current terminal only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment using that project's activation command.

## Project 1: IT Incident Routing

The workflow reads incidents from `model_agent\incidents.json`, uses a triage agent to classify severity, and routes the incident to either the escalation agent or the resolution agent.

### Setup and install

```powershell
cd "C:\Users\Trainer\Downloads\AI TRAINIG\Day27\model_agent"
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Configure Azure

Create a file named `.env` inside `model_agent`:

```dotenv
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_BASE_URL=https://<your-resource>.openai.azure.com/openai/v1
AZURE_OPENAI_MODEL=<your-deployment-name>
```

Replace the example values with your actual endpoint and deployment. Keep the API key private; do not commit `.env` to source control.

### Run

```powershell
python graph_workflow.py
```

## Project 2: Vendor Purchase Approval

This project reads `vendor_approval_workflow\purchases.json`. The Procurement Agent reviews the justification, the Risk Agent assesses risk, and the approval gateway automatically approves eligible requests or pauses for a manager response. The final agent creates a demo decision record.

### Setup and install

```powershell
cd "C:\Users\Trainer\Downloads\AI TRAINIG\Day27\vendor_approval_workflow"
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Configure Azure

Create a file named `.env` inside `vendor_approval_workflow`:

```dotenv
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_BASE_URL=https://<your-resource>.openai.azure.com/openai/v1
AZURE_OPENAI_MODEL=<your-deployment-name>
```

Keep the API key private.

### Run

```powershell
python workflow.py
```

When the program requests manager approval, enter `approve` or `reject` in the terminal.

## Project 3: E-commerce Returns

This project reads the ten customer requests in `Ecommerce_agent_assignment\returns.json`. Deterministic Python rules enforce the demo return policy. Requests that do not meet every automatic approval condition require a human manager decision.

Automatic approval requires all of the following:

1. The item amount is below INR 25,000.
2. The return is within 30 days after delivery.
3. An invoice is available.
4. The item is unopened, or it is damaged and photo evidence is available.
5. The customer has fewer than three previous returns in the last 90 days.
6. The assessed risk is not HIGH.

### Setup and install

```powershell
cd "C:\Users\Trainer\Downloads\AI TRAINIG\Day27\Ecommerce_agent_assignment"
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Configure Azure (optional)

To enable AI agent assessments, create a file named `.env` inside `Ecommerce_agent_assignment`:

```dotenv
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_BASE_URL=https://<your-resource>.openai.azure.com/openai/v1
AZURE_OPENAI_MODEL=<your-deployment-name>
```

Without these values, the project uses deterministic policy evaluation and still prompts for manager decisions when a request needs review. Keep the API key private.

### Run

```powershell
python workflow.py
```

The output is a simulation. It does not process payments, send customer messages, or initiate replacements.

## Selecting the correct VS Code interpreter

If Pylance reports that imports such as `dotenv`, `openai`, or `agent_framework` cannot be resolved:

1. Open the project folder in VS Code.
2. Press **Ctrl+Shift+P** and select **Python: Select Interpreter**.
3. Choose that project's environment:
   - `model_agent\.venv\Scripts\python.exe`
   - `vendor_approval_workflow\.venv\Scripts\python.exe`
   - `Ecommerce_agent_assignment\.venv\Scripts\python.exe`
4. If diagnostics remain stale, run **Developer: Reload Window**.

To install dependencies again in an activated environment:

```powershell
python -m pip install -r requirements.txt
```

Run this command from the project directory whose dependencies you want to install.

## Security and cost notes

- Never place real API keys in Python files or commit `.env` files.
- AI-enabled runs make requests to Azure and may incur usage charges.
- The purchase and returns projects are demonstrations; do not treat their outputs as completed real-world transactions.
