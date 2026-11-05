import os
import json 
from openai import OpenAI
from dotenv import load_dotenv
#import the tools
from tools import search_books, reserve_book

#2.get api key and model from .env file

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
model_name=os.getenv("OPENROUTER_MODEL")


#3.intialize the OpenAI clientimport os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 1. Import the tools
from tools import search_books, reserve_book

# 2. Get API key and model from .env file
#    override=True makes .env win over any old Windows environment variables
load_dotenv(override=True)
api_key = os.getenv("OPENROUTER_API_KEY")
model_name = os.getenv("OPENROUTER_MODEL")

if not api_key or not model_name:
    raise SystemExit("Set OPENROUTER_API_KEY and OPENROUTER_MODEL in .env first.")

# 3. Initialise the client - base_url sends requests to OpenRouter, not OpenAI
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)

MAX_STEPS = 5  # safety limit so the agent can't loop forever

# 4. Define the tools for the AI model
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "search_books",
            "description": "Search for books in the library database",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "The keyword to search for in book titles, authors, or categories.",
                    }
                },
                "required": ["keyword"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "reserve_book",
            "description": "Reserve a book in the library",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {
                        "type": "integer",
                        "description": "The ID of the book to reserve.",
                    },
                    "customer_name": {
                        "type": "string",
                        "description": "The name of the customer reserving the book.",
                    },
                },
                "required": ["book_id", "customer_name"],
            },
        },
    },
]


def run_tool(function_name, function_args):
    """Run the requested tool and always return a string."""
    try:
        if function_name == "search_books":
            result = search_books(keyword=function_args.get("keyword"))
        elif function_name == "reserve_book":
            result = reserve_book(
                book_id=function_args.get("book_id"),
                customer_name=function_args.get("customer_name"),
            )
        else:
            result = f"Error: Tool '{function_name}' not recognized."
    except Exception as e:
        result = f"Error while running {function_name}: {e}"

    # Tool results sent back to the model must be text
    return result if isinstance(result, str) else json.dumps(result, default=str)


def chat_with_agent():
    # Keep track of the conversation history
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful library assistant. You can search for books and reserve them "
                "for customers. Use the provided tools to perform these actions. "
                "Before reserving, make sure you know the book ID and the customer's name; "
                "ask the user if either is missing."
            ),
        }
    ]

    while True:
        # Step a: accept question from user
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat. Goodbye!")
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        # Agent loop: repeat until the model gives a final answer
        for step in range(MAX_STEPS):
            # Step b: send the conversation to the AI model (new 'tools' format)
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                tools=tools_schema,
                tool_choice="auto",
            )
            response_message = response.choices[0].message

            # Step c: no tool requested -> final answer
            if not response_message.tool_calls:
                final_answer = response_message.content or ""
                messages.append({"role": "assistant", "content": final_answer})
                print(f"\nLibrary AI Agent: {final_answer}")
                break

            # Save the model's tool request in the history as a plain dict
            messages.append({
                "role": "assistant",
                "content": response_message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in response_message.tool_calls
                ],
            })

            # Step d: run every requested tool
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                try:
                    function_args = json.loads(tool_call.function.arguments or "{}")
                except json.JSONDecodeError:
                    function_args = {}

                print(f"\n>>> [agent] Calling tool: {function_name} with arguments: {function_args}")
                tool_result = run_tool(function_name, function_args)

                # Step e: send the tool result back to the model
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                })
            # Loop again so the model can read the results and answer (or call more tools)
        else:
            print("\nLibrary AI Agent: Sorry, I couldn't finish that request. Please try rephrasing it.")


if __name__ == "__main__":
    chat_with_agent()
client=OpenAI(api_key=api_key)


#4.define the tools for the ai model
tools_schema=[{
    "type": "function",
    "function": {
        "name": "search_books",
        "description": "Search for books in the library database",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "The keyword to search for in book titles, authors, or categories."}
            },
            "required": ["keyword"]
        }
    }
}, 
{
    "type": "function",

    "function": {

        "name": "reserve_book",
        "description": "Reserve a book in the library",
        "parameters": {
            "type": "object",
            "properties": {
                "book_id": {
                    "type": "integer",
                    "description": "The ID of the book to reserve."
                },
                "customer_name": {
                    "type": "string",
                    "description": "The name of the customer reserving the book."
                }
            },
            "required": ["book_id", "customer_name"]
        }
    }
}
]


def chat_with_agen():
    #keep track of the conversation history
    messages=[
        {
            "role": "system",
            "content": "You are a helpful library assistant. You can search for books and reserve them for customers. Use the provided tools to perform these actions."
        }
    ]


    while True:
        #step a:accept question from user
        user_input=input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat. Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        #step b:send the question to the ai model
        response=client.chat.completions.create(
            model=model_name,
            messages=messages,
            functions=tools_schema,
            function_call="auto"
        )
        response_message=response.choices[0].message

        #step c:check if the ai model wants to call a tool
        if response_message.tool_calls:
            messages.append(response_message)

            for tool_call in response_message.tool_calls:
                function_name=tool_call.name
                function_args=json.loads(tool_call.function.arguments)

                print(f"\n>>>[agent] Calling tool: {function_name} with arguments: {function_args}")
                #step d:execute the tool and get the result
                if function_name=="search_books":
                    tool_result=search_books(keyword=function_args.get("keyword"))

                elif function_name=="reserve_book":
                    tool_result=reserve_book(
                        book_id=function_args.get("book_id"),
                        customer_name=function_args.get("customer_name")
                    )
                else:
                    tool_result=f"Error: Tool '{function_name}' not recognized."

                #step e:send the tool result back to the ai model
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": tool_result
                })

                #step f:send the tool result back to the ai model for final responsese
                second_response=client.chat.completions.create(
                        model=model_name,
                        messages=messages
                )
                final_answer=second_response.choices[0].message.content
                messages.append({"role": "assistant", "content": final_answer})
                print(f"\nLibrary AI Agent: {final_answer}")
        else:
            print(f"\nLibrary AI Agent: {response_message.content}")
            messages.append({"role": "assistant", "content": response_message.content})

if __name__=="__main__":
    chat_with_agen()