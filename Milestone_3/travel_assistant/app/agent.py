import json
from typing import Any

import httpx
from ollama import ResponseError
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.memory import history_as_text
from app.tools import trip_lookup, weather_lookup


class ModelUnavailableError(RuntimeError):
    pass


def _make_chain():
    model = ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0,
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a practical business travel advisor. Use only the trip and "
                "forecast facts supplied below; never make up weather, dates, or trip "
                "details. If forecast status is error, clearly say live forecast data "
                "is unavailable and do not infer conditions. Give a concise answer "
                "and, when relevant, 3-4 practical packing or travel suggestions. "
                "Use the conversation history to understand follow-up questions.",
            ),
            (
                "human",
                "Saved trip (from trip lookup tool):\n{trip}\n\n"
                "Forecast (from weather tool):\n{weather}\n\n"
                "Recent conversation:\n{history}\n\n"
                "Employee question: {question}",
            ),
        ]
    )
    return prompt | model | StrOutputParser()


def generate_advice(
    trip_id: int,
    question: str,
    history: list[dict[str, Any]],
) -> dict[str, Any]:
    trip_result = json.loads(trip_lookup.invoke({"trip_id": trip_id}))
    if trip_result.get("status") != "ok":
        raise LookupError(trip_result.get("message", "Trip lookup failed."))

    trip = trip_result["trip"]
    weather = json.loads(
        weather_lookup.invoke(
            {
                "destination": trip["destination"],
                "start_date": trip["start_date"],
                "end_date": trip["end_date"],
            }
        )
    )

    try:
        answer = _make_chain().invoke(
            {
                "trip": json.dumps(trip, ensure_ascii=False),
                "weather": json.dumps(weather, ensure_ascii=False),
                "history": history_as_text(history),
                "question": question,
            }
        )
    except (httpx.HTTPError, ResponseError, ValueError) as exc:
        raise ModelUnavailableError(
            f"Could not reach Ollama at {OLLAMA_BASE_URL} or load model "
            f"'{OLLAMA_MODEL}'. Install and start Ollama, then run "
            f"`ollama pull {OLLAMA_MODEL}`."
        ) from exc

    return {"answer": answer, "weather": weather}
