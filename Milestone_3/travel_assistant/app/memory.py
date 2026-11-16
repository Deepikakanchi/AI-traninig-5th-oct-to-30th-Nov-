import hashlib
import json
from typing import Any

import redis

from app.config import (
    REDIS_MAX_HISTORY_MESSAGES,
    REDIS_SESSION_TTL_SECONDS,
    REDIS_URL,
)

_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)


def _session_key(session_id: str) -> str:
    digest = hashlib.sha256(session_id.encode("utf-8")).hexdigest()
    return f"travel-weather:session:{digest}:history"


def get_history(session_id: str) -> list[dict[str, str]]:
    entries = _client.lrange(_session_key(session_id), 0, -1)
    return [json.loads(entry) for entry in entries]


def save_exchange(session_id: str, question: str, answer: str) -> None:
    key = _session_key(session_id)
    with _client.pipeline() as pipeline:
        pipeline.rpush(
            key,
            json.dumps({"role": "user", "content": question}),
            json.dumps({"role": "assistant", "content": answer}),
        )
        pipeline.ltrim(key, -REDIS_MAX_HISTORY_MESSAGES, -1)
        pipeline.expire(key, REDIS_SESSION_TTL_SECONDS)
        pipeline.execute()


def history_as_text(history: list[dict[str, Any]]) -> str:
    return "\n".join(
        f"{message['role']}: {message['content']}" for message in history
    )
