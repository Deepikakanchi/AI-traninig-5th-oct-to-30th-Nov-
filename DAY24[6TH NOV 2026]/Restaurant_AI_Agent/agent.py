import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from guardrails import is_restaurant_related, redact_pii, validate_input

#import the tools
from tools import search_restaurants, calculate_dining_cost

#load environment variables from .env file
load_dotenv()

# Create the model using OpenRouter when its key is configured; otherwise keep
# supporting the standard OpenAI configuration.
openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()

if openrouter_api_key:
    api_key = openrouter_api_key
    model_name = os.getenv("OPENROUTER_MODEL", "").strip() or "openrouter/free"
    base_url = "https://openrouter.ai/api/v1"
elif openai_api_key:
    api_key = openai_api_key
    model_name = os.getenv("OPENAI_MODEL", "").strip() or "gpt-4o-mini"
    base_url = os.getenv("OPENAI_BASE_URL") or None
else:
    raise RuntimeError(
        "No API key found. Set OPENROUTER_API_KEY in .env to use OpenRouter "
        "or OPENAI_API_KEY to use OpenAI."
    )

model = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    temperature=0,
    base_url=base_url,
)
checkpointer = InMemorySaver()

#create an agent with the model and tools
agent = create_agent(
    model=model,
    tools=[search_restaurants, calculate_dining_cost],
    checkpointer=checkpointer,
    system_prompt=(
        "You are a restaurant assistant that helps users find restaurants and calculate dining costs. "
        "Help users find restaurants based on cuisine type or keywords, and calculate the total dining cost "
        "based on restaurant ID and number of guests. Use the tools provided to perform these tasks. "
        "If the user asks for something outside of your capabilities, respond with "
        "'I am sorry, I cannot assist with that request.' "
        "Never invent restaurant, cuisine, or price information. Only provide information from the restaurant JSON file. "
        "CRITICAL RULE: Do not process actual reservation bookings or payments. Only provide information and "
        "calculations based on the restaurant data. If a user tries to book a reservation or make a payment, "
        "respond with 'I am sorry, I cannot assist with that request.'"
    )
)

#run application
if __name__ == "__main__":
    thread_number = 1
    previous_count = 0
    has_restaurant_context = False
    print("Welcome to the Restaurant Assistant!")
    while True:
        question = input("\nyou: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("Exiting the Restaurant Assistant. Goodbye!")
            break
        if question.lower() == "/new":
            thread_number += 1
            previous_count = 0
            has_restaurant_context = False
            print(f"\nStarting a new conversation thread: Thread {thread_number}")
            continue
        is_valid, validation_message = validate_input(question)
        if not is_valid:
            print(f"\nAgent: {validation_message}")
            continue
        if not is_restaurant_related(question, has_context=has_restaurant_context):
            print("\nAgent: I can only help with restaurant-related questions.")
            continue
        has_restaurant_context = True
        config = {
            "configurable": {
                "thread_id": f"restaurant-chat-{thread_number}"
            }
        }

        try:
            result = agent.invoke(
                {
                    "messages":[
                        {"role":"user","content":question}
                    ]
                },
                config=config
            )
            messages = result["messages"]
            new_messages = messages[previous_count:]
            previous_count = len(messages)

            for message in new_messages:
                if isinstance(message, AIMessage):
                    for call in message.tool_calls:
                        print(f"\n[Tool selected]: {call['name']}")
                        print(f"[arguments]: {redact_pii(str(call['args']))}")

                if isinstance(message, ToolMessage):
                    print(f"[TOOL RESULT]: {redact_pii(str(message.content))}")
            print(f"\nAgent: {redact_pii(str(messages[-1].content))}")

        except Exception as error:
            print(f"Error: {error}")
            