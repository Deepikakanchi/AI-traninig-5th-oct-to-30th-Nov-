# Ecommerce Multi-Agent Assistant

A command-line ecommerce assistant that searches a local product catalog, checks requested quantities against stock and budget, and recommends the highest-rated eligible product.

## Requirements

- Python
- An [OpenRouter API key](https://openrouter.ai/settings/keys)

The configured model must be available to your OpenRouter account and support chat completions and tool calling. The example below uses `openai/gpt-4.1-mini`.

## Setup on Windows

Open PowerShell in the project directory and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in the project directory with your own OpenRouter key and model:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=openai/gpt-4.1-mini
```

Do not share or commit `.env`. If a key is exposed, revoke it in OpenRouter and create a replacement.

## Run

```powershell
python sequential.py
```

Enter requests at the prompt. Submit a blank line to exit. For example:

```text
Recommend 2 laptops within ₹1,20,000 total.
Find 3 smartphones within ₹1,00,000 total.
Find 100 laptops and verify stock availability.
```

Requests that ask for a recommendation should include a product category, quantity, and total budget. The product catalog is stored in `products.json`; prices and stock are reported from that file.

## Project files

- `sequential.py` — starts the command-line loop and runs the agents in sequence.
- `agents.py` — defines the inventory, pricing, and recommendation agents.
- `tools.py` — product search, order-total tool, and formatted customer report.
- `products.json` — local product catalog.
- `requirements.txt` — Python package dependencies.
