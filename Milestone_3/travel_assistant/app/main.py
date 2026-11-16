from contextlib import asynccontextmanager
from typing import Any

import redis
from fastapi import FastAPI, HTTPException

from app import db, memory
from app.agent import ModelUnavailableError, generate_advice
from app.schemas import AskRequest, TripCreate


@asynccontextmanager
async def lifespan(_: FastAPI):
    db.init_db()
    yield


app = FastAPI(
    title="AI-Powered Travel & Weather Advisory Assistant",
    description="Trip planning API with SQLite, Redis, Open-Meteo and LangChain/Ollama.",
    lifespan=lifespan,
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Travel Weather Assistant is running."}


@app.post("/trips", status_code=201)
def create_trip(payload: TripCreate) -> dict[str, Any]:
    trip = db.create_trip(
        employee_id=payload.employee_id,
        destination=payload.destination,
        start_date=payload.start_date.isoformat(),
        end_date=payload.end_date.isoformat(),
        purpose=payload.purpose,
        session_id=payload.session_id,
    )
    return {
        "trip_id": trip["id"],
        "status": "created",
        "trip": trip,
        "session_id": payload.session_id,
    }


@app.get("/trips/{trip_id}")
def get_trip(trip_id: int) -> dict[str, Any]:
    trip = db.get_trip_by_id(trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found.")
    return trip


@app.post("/ask")
def ask_assistant(payload: AskRequest) -> dict[str, Any]:
    if payload.trip_id is not None:
        trip = db.get_trip_by_id(payload.trip_id)
        if trip is None:
            raise HTTPException(status_code=404, detail="Trip not found.")
        db.bind_trip_to_session(payload.session_id, payload.trip_id)
    else:
        trip = db.get_trip_for_session(payload.session_id)
        if trip is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    "No trip is linked to this session. Create a trip with this "
                    "session_id or include trip_id in the request."
                ),
            )

    try:
        history = memory.get_history(payload.session_id)
        result = generate_advice(trip["id"], payload.question, history)
        memory.save_exchange(payload.session_id, payload.question, result["answer"])
    except redis.RedisError as exc:
        raise HTTPException(
            status_code=503,
            detail="Redis is unavailable. Start Redis and retry the request.",
        ) from exc
    except ModelUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    weather = result["weather"]
    return {
        "session_id": payload.session_id,
        "trip_id": trip["id"],
        "answer": result["answer"],
        "weather": weather,
        "weather_summary": weather.get("summary", weather.get("message")),
    }
