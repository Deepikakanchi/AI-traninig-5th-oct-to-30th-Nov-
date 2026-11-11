# Azure AI Foundry Agent CLI

This project is a lightweight Python command-line application that connects to an existing Azure AI Foundry (formerly Azure AI Studio / Microsoft Foundry) project and chats with a configured agent using the Azure Python SDK.

It is designed for quick interactive testing, local experimentation, and lightweight agent-based support workflows where you already have a deployed Azure AI Foundry project and agent.

## Overview

The application:

- loads environment variables from a `.env` file
- authenticates to Azure using `DefaultAzureCredential`
- connects to an existing Microsoft Foundry project using `AIProjectClient`
- retrieves an existing agent named by `FOUNDRY_AGENT_NAME` or defaults to `RetailSupportAgent`
- creates a conversation session
- sends user prompts to the agent and prints the response
- keeps running in a loop until the user types `exit`

## Project Structure

```text
azure_agent/
├── main.py
├── requirements.txt
├── .env.example      (recommended to create locally)
├── .env              (local, not committed)
└── README.md
```

## Prerequisites

Before running this project, make sure you have:

- Python 3.9 or newer
- An Azure subscription
- Access to an Azure AI Foundry project
- A deployed or configured AI agent in that project
- Azure CLI installed and authenticated (`az login`), or another supported authentication method for `DefaultAzureCredential`

## Required Azure Setup

You need an existing Azure AI Foundry project endpoint. The code expects the following environment variable:

- `FOUNDRY_PROJECT_ENDPOINT`: URL of your Azure AI Foundry project endpoint

Optional:

- `FOUNDRY_AGENT_NAME`: name of the agent you want to use. If not set, the app defaults to `RetailSupportAgent`

You must also ensure your identity has permission to access that Azure AI project.

## Installation

1. Open a terminal in the project folder.
2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment:

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

macOS/Linux:

```bash
source .venv/bin/activate
```

4. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root with the following contents:

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-endpoint>
FOUNDRY_AGENT_NAME=RetailSupportAgent
```

Example:

```env
FOUNDRY_PROJECT_ENDPOINT=https://myproject.services.ai.azure.com/api/projects/myproject
FOUNDRY_AGENT_NAME=RetailSupportAgent
```

Important notes:

- `.env` should not be committed to source control if it contains real Azure values.
- The project loads these variables using `python-dotenv`.

## Authentication

This application uses `DefaultAzureCredential` from the Azure Identity library. That means it can authenticate through a chain of supported sources, such as:

- environment variables
- Azure CLI login (`az login`)
- managed identity / workload identity
- Visual Studio / Azure Developer CLI credentials

For local development, the most common setup is:

```bash
az login
```

Then run the Python script. If Azure CLI authentication is available and your account has access to the project, the script will connect successfully.

## Running the Application

From the project root:

```bash
python main.py
```

Example interaction:

```text
Connected to RetailSupportAgent
Type exit to quit

You: What are the best products for a small business?

Agent: Here are some options based on your requirements...

You: exit
```

## How It Works

The script does the following in order:

1. Loads environment values from `.env` using `load_dotenv()`.
2. Creates an `AIProjectClient` using:
   - the project endpoint
   - `DefaultAzureCredential()`
   - `allow_preview=True`
3. Calls `project.get_openai_client()` to get the client needed for interacting with the agent.
4. Creates a new conversation via `client.conversations.create()`.
5. Enters a loop where it reads user input.
6. Sends each prompt to the agent using:

```python
response = client.responses.create(
    conversation=conversation.id,
    input=question
)
```

7. Prints `response.output_text` to the terminal.

## Dependency Details

The project dependencies are defined in `requirements.txt`:

```txt
azure-ai-projects>=2.9.0
azure-identity
python-dotenv
```

These packages provide:

- Azure AI Foundry client access
- Azure authentication
- environment variable loading from `.env`

## Troubleshooting

### 1. `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'`

This happens when the environment variable is missing.

Fix:

- create a `.env` file
- confirm the variable name matches exactly
- restart the script after saving the file

### 2. Authentication failures

If `DefaultAzureCredential` fails, use:

```bash
az login
```

If you are running in Azure, ensure the managed identity or service principal is correctly configured.

### 3. Access denied / 403 errors

This usually means your Azure identity does not have permission to the Azure AI Foundry project.

Fix:

- verify you are signed in with the correct Azure user or service principal
- confirm you were granted access to the project
- check that the project endpoint is correct

### 4. Agent not found

If the configured agent name does not exist, the script may fail when attempting to access it.

Fix:

- verify `FOUNDRY_AGENT_NAME`
- confirm the agent exists in the Azure AI Foundry project
- use the exact agent name configured in the project

## Security Best Practices

- Do not commit `.env` files to source control.
- Store sensitive configuration in a secure environment or secret manager.
- Limit Azure roles to the least privilege required.
- Avoid hardcoding project endpoints or credentials directly in code.

## Example Use Cases

This project is useful for:

- testing a Foundry agent interactively
- creating a local prototype for AI-based customer support
- validating agent behavior before integrating it into a larger application
- quick debugging and prompt experimentation

## Notes

This project is intentionally minimal and built around direct interaction with an existing Azure AI Foundry agent. It is not a web app, API service, or production deployment scaffold. It is best suited for local experimentation or lightweight CLI tooling.

## Future Enhancements

Potential improvements include:

- support for multiple agents with a menu
- adding command-line arguments instead of only environment variables
- chat history export
- better error handling and logging
- support for streaming responses
- a web or REST wrapper around the same agent interaction flow

## License

This project does not currently include a license file. If you plan to share or distribute it, add an appropriate open-source license according to your organization's requirements.
