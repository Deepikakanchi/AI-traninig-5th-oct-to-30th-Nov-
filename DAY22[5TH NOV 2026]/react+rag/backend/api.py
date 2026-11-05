import json
import os
import re

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field

from tools import BOOKS_FILE, read_json_file, reserve_book, search_books

load_dotenv(override=True)
api_key = os.getenv("OPENROUTER_API_KEY")
model_name = os.getenv("OPENROUTER_MODEL")

if not api_key or not model_name:
    raise SystemExit("Set OPENROUTER_API_KEY and OPENROUTER_MODEL in .env first.")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    history: list[dict[str, str]] = Field(default_factory=list)
    pending_reservation: dict | None = None


class ConfirmationRequest(BaseModel):
    book_id: int
    customer_name: str
    confirmed: bool = True


TOOLS_SCHEMA = [
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
            "description": "Reserve a book in the library after the customer confirms the reservation",
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


def _run_tool(function_name: str, function_args: dict):
    if function_name == "search_books":
        return search_books(keyword=function_args.get("keyword", ""))
    if function_name == "reserve_book":
        return (
            "Reservation request received for "
            f"book_id={function_args.get('book_id')} and customer_name={function_args.get('customer_name')}. "
            "The book is available. Please confirm your reservation."
        )
    return f"Error: Tool '{function_name}' not recognized."


def _find_book(message: str, history: list[dict[str, str]]):
    books = read_json_file(BOOKS_FILE)
    current_words = set(re.findall(r"[a-z0-9]+", message.lower()))
    history_text = " ".join(
        entry.get("content", "")
        for entry in history[-8:]
        if entry.get("role") in {"user", "assistant"}
    ).lower()
    history_words = set(re.findall(r"[a-z0-9]+", history_text))
    ignored_words = {"the", "a", "an", "book", "reserve", "reservation", "please", "for", "this"}

    ranked_books = []
    for book in books:
        title_words = set(re.findall(r"[a-z0-9]+", book["title"].lower())) - ignored_words
        current_matches = title_words & current_words
        history_matches = title_words & history_words
        score = len(current_matches) * 2 + len(history_matches)
        if title_words and score:
            ranked_books.append((score, len(current_matches), book))

    if not ranked_books:
        return None

    ranked_books.sort(key=lambda item: (item[0], item[1]), reverse=True)
    best = ranked_books[0]
    if len(ranked_books) > 1 and ranked_books[1][:2] == best[:2]:
        return None
    return best[2]


def _customer_name(message: str, allow_bare: bool = False):
    match = re.search(r"\bfor\s+(.+?)\s*$", message.strip(), flags=re.IGNORECASE)
    if not match:
        if allow_bare:
            name = re.sub(r"[.!?]+$", "", message.strip())
            if re.fullmatch(r"[A-Za-z][A-Za-z '-]{0,59}", name):
                return name
        return None
    name = re.sub(r"[.!?]+$", "", match.group(1)).strip()
    if name.lower() in {"this", "me", "myself", "the book"}:
        return None
    return name or None


def _reservation_response(book: dict, customer_name: str | None):
    if book["available_copies"] <= 0:
        return {
            "response": f"Sorry, {book['title']} is currently unavailable.",
            "tool_used": "search_books",
            "status": "success",
            "pending_reservation": None,
        }

    pending = {
        "book_id": book["id"],
        "title": book["title"],
        "customer_name": customer_name,
    }
    if customer_name:
        answer = (
            f"{book['title']} is available ({book['available_copies']} copies). "
            f"Please confirm the reservation for {customer_name}."
        )
    else:
        answer = (
            f"{book['title']} is available ({book['available_copies']} copies). "
            "Who should I put on the reservation?"
        )
    return {
        "response": answer,
        "tool_used": "reserve_book",
        "status": "success",
        "pending_reservation": pending,
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Handle messages from the chat UI and perform tool-backed library actions."""
    message_text = request.message.strip()
    pending = request.pending_reservation

    if pending:
        customer_name = pending.get("customer_name") or _customer_name(message_text, allow_bare=True)
        book = next(
            (item for item in read_json_file(BOOKS_FILE) if item["id"] == pending.get("book_id")),
            None,
        )
        if book:
            return _reservation_response(book, customer_name)

    if re.search(r"\b(reserv(e|ation)|book\s+for)\b", message_text, flags=re.IGNORECASE):
        book = _find_book(message_text, request.history)
        if book:
            return _reservation_response(book, _customer_name(message_text))
        return {
            "response": "I couldn't identify the book to reserve. Please include its title or author.",
            "tool_used": None,
            "status": "success",
            "pending_reservation": None,
        }

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful library assistant. Use the provided tools to search for books and "
                "reserve them for customers. Ask for confirmation before finalizing a reservation. "
                "Do not reserve a book until the customer explicitly confirms."
            ),
        },
    ]
    for entry in request.history[-12:]:
        if entry.get("role") in {"user", "assistant"} and entry.get("content"):
            messages.append({"role": entry["role"], "content": entry["content"]})
    messages.append({"role": "user", "content": request.message})

    last_tool_name = None
    pending_reservation = None

    for _ in range(5):
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=TOOLS_SCHEMA,
            tool_choice="auto",
        )
        message = response.choices[0].message

        if not message.tool_calls:
            final_response = message.content or "I couldn't complete that request."
            return {
                "response": final_response,
                "tool_used": last_tool_name,
                "status": "success",
                "pending_reservation": pending_reservation,
            }

        last_tool_name = message.tool_calls[0].function.name
        messages.append(
            {
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                    for tool_call in message.tool_calls
                ],
            }
        )

        for tool_call in message.tool_calls:
            try:
                function_args = json.loads(tool_call.function.arguments or "{}")
            except json.JSONDecodeError:
                function_args = {}

            if (
                tool_call.function.name == "reserve_book"
                and isinstance(function_args.get("book_id"), int)
                and isinstance(function_args.get("customer_name"), str)
                and function_args["customer_name"].strip()
            ):
                pending_reservation = {
                    "book_id": function_args["book_id"],
                    "customer_name": function_args["customer_name"].strip(),
                }

            tool_result = _run_tool(tool_call.function.name, function_args)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                }
            )

    return {
        "response": "Sorry, I couldn't finish that request. Please try rephrasing it.",
        "tool_used": last_tool_name,
        "status": "error",
        "pending_reservation": pending_reservation,
    }


@app.post("/confirm-reservation")
async def confirm_reservation(request: ConfirmationRequest):
    if not request.confirmed:
        return {
            "response": "Reservation cancelled.",
            "status": "cancelled",
            "book_id": request.book_id,
            "customer_name": request.customer_name,
        }

    result = reserve_book(book_id=request.book_id, customer_name=request.customer_name)
    return {
        "response": result,
        "status": "success" if result.startswith("Reservation successful") else "error",
        "book_id": request.book_id,
        "customer_name": request.customer_name,
    }
