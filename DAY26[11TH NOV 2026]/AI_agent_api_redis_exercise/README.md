# Employee Leave Support Agent (CLI)

This project is a lightweight command-line chatbot that connects to an existing Microsoft Foundry project and uses the `EmployeeLeaveAgent` agent to answer employee leave-related questions. It does not expose an HTTP API, does not use Redis, and is designed to run locally from your terminal.

This README explains how to set up, configure, and run the project in a clear step-by-step way.

## What this project does

The app:

- loads environment settings from a local `.env` file
- authenticates to Azure using `DefaultAzureCredential()`
- connects to your Microsoft Foundry project using `AIProjectClient`
- opens a client for the named agent (`EmployeeLeaveAgent` by default)
- creates a conversation and lets you ask questions from the command line
- sends each question to the agent and prints the response

The main execution flow is in `main.py`.

## Project files

- `main.py` - CLI app entry point
- `requirements.txt` - Python package dependencies
- `.env` - local environment settings (not tracked in Git)

## Requirements

Before you start, make sure you have:

- Windows 10 or later
- Python 3.14 recommended
- Azure CLI installed and available in PATH
- Access to an Azure/Microsoft Foundry project that contains the `EmployeeLeaveAgent`
- Permission to authenticate with Azure using your signed-in account

Important:

- Python 3.16 may not work cleanly with the current dependency set, so 3.14 is recommended.
- Keep your `.env` file local and private. Never commit secrets or endpoint values to source control.

## Step-by-step setup

### 1. Open a terminal in the project folder

Open PowerShell in the folder that contains `main.py` and `requirements.txt`.

### 2. Create a virtual environment

```powershell
py -3.14 -m venv .venv
```

If `py -3.14` is not available on your machine, use the Python 3.14 interpreter you already installed in VS Code or your system.

### 3. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run this once for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 4. Upgrade pip and install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

This installs:

- `azure-ai-projects`
- `azure-identity`
- `python-dotenv`

### 5. Sign in to Azure

The project uses Azure identity for authentication, so you must sign in to Azure CLI first:

```powershell
az login
```

If your organization uses multiple Azure subscriptions, make sure the correct one is selected:

```powershell
az account list -o table
az account set --subscription "<your-subscription-name-or-id>"
```

### 6. Create a `.env` file

Create a file named `.env` in the same folder as `main.py` with the following content:

```dotenv
FOUNDRY_PROJECT_ENDPOINT=<your Microsoft Foundry project endpoint>
FOUNDRY_AGENT_NAME=EmployeeLeaveAgent
```

Example:

```dotenv
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-endpoint>.services.ai.azure.com/api/projects/<project-name>
FOUNDRY_AGENT_NAME=EmployeeLeaveAgent
```

Use your actual Microsoft Foundry project endpoint and agent name. If needed, confirm the exact values in the Foundry portal or project configuration.

### 7. Run the app

Start the chatbot:

```powershell
python main.py
```

After the app starts, you should see a prompt similar to:

```text
Connected to EmployeeLeaveAgent
Type exit to quit
```

### 8. Chat with the agent

At the `You:` prompt, type a question and press Enter.

Example:

```text
You: How many days of annual leave do employees get?
```

The app sends your question to the connected agent and prints the response.

To exit the program, type:

```text
exit
```

## How the app works internally

The program does the following:

1. Loads variables from `.env` using `load_dotenv()`.
2. Creates an `AIProjectClient` with:
   - your Foundry project endpoint
   - `DefaultAzureCredential()` for authentication
   - `allow_preview=True`
3. Retrieves the agent client using `project.get_openai_client()` and the agent name.
4. Creates a conversation with `client.conversations.create()`.
5. Reuses that same conversation for all prompts during the run.
6. Sends each user message with `client.responses.create(...)`.
7. Prints `response.output_text`.

This means the app keeps one chat thread active while the terminal session stays open.

## Troubleshooting

### `ModuleNotFoundError` or package install issue

Make sure the virtual environment is active and that you installed dependencies from the project folder:

```powershell
python -m pip install -r requirements.txt
```

### Azure authentication errors

If you see authentication-related errors, sign in again:

```powershell
az login
```

If you are in a multi-subscription environment, select the correct one:

```powershell
az account list -o table
az account set --subscription "<subscription-id-or-name>"
```

### `.env` not being loaded

Make sure:

- the file is named exactly `.env`
- it is in the same folder as `main.py`
- it contains valid key/value pairs with no extra spaces or quoting issues

### The app cannot find the agent

Check that:

- the project endpoint is correct
- the agent name matches the actual Foundry agent name
- your Azure account has access to the Foundry project

### PowerShell activation is blocked

Use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Important notes

- This project is a local CLI tool, not a web service.
- It depends on an existing Microsoft Foundry project and agent configuration.
- The chat session remains alive for the duration of one terminal run.
- Keep your environment data private and do not expose `.env` contents in public repositories.

## Quick start summary

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
az login
python main.py
```

Then create `.env` with your Foundry project endpoint and start chatting.
