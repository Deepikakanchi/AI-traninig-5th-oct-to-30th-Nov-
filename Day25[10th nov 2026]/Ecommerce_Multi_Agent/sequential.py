import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from agent_framework.openai import OpenAIChatCompletionClient
from agent_framework_orchestrations import SequentialBuilder

from agents import (
    create_inventory_agent,
    create_pricing_agent,
    create_recommendation_agent,
)
from tools import build_customer_report

#1. Execute the three agents in the specified order.

def create_sequential_workflow(chat_client: OpenAIChatCompletionClient):
    """Build the workflow with inventory, pricing, and recommendations in order."""
    inventory_agent = create_inventory_agent(chat_client)
    pricing_agent = create_pricing_agent(chat_client)
    recommendation_agent = create_recommendation_agent(chat_client)

    return SequentialBuilder(
        participants=[
            inventory_agent,
            pricing_agent,
            recommendation_agent,
        ],
        chain_only_agent_responses=False,  #2. Pass relevant conversation context between agents.
        output_from="all",   #5. Display the intermediate results of all three agents
        ensure_trailing_user_turn=True,
    ).build()


#4. Execute the workflow asynchronously.
async def run_workflow(chat_client: OpenAIChatCompletionClient, customer_request: str):
    """Run the sequential workflow asynchronously for a customer request."""
    print()
    print(build_customer_report(customer_request))

    workflow = create_sequential_workflow(chat_client)
    stream = workflow.run(customer_request, stream=True)#Important: Implement the orchestration using SequentialBuilder . Do not manually call three agents one after another using separate run() statements.

    async for _ in stream:
        pass
    final_result = await stream.get_final_response()

    return final_result


async def main():
    """Run customer requests one at a time until the user submits a blank line."""
    load_dotenv(Path(__file__).with_name(".env"))

    required_settings = ("OPENROUTER_API_KEY", "OPENROUTER_MODEL")
    missing_settings = [name for name in required_settings if not os.getenv(name)]
    if missing_settings:
        raise RuntimeError(
            "Missing required .env setting(s): " + ", ".join(missing_settings)
        )

    chat_client = OpenAIChatCompletionClient(
        model=os.environ["OPENROUTER_MODEL"],
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
    )

    print("Enter a customer request. Submit a blank line to exit.")
    while True:
        customer_request = input("\nCustomer request: ").strip()
        if not customer_request:
            print("Exiting.")
            break
        await run_workflow(chat_client, customer_request)


if __name__ == "__main__":
    asyncio.run(main())
