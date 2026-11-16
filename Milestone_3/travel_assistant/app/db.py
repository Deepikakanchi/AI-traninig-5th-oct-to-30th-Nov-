import sqlite3
from contextlib import contextmanager
from typing import Any, Generator, Optional

from app.config import DATABASE_PATH, PROJECT_ROOT


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_db() -> None:
    schema = (PROJECT_ROOT / "schema.sql").read_text(encoding="utf-8")
    with get_connection() as connection:
        connection.executescript(schema)


def create_trip(
    employee_id: str,
    destination: str,
    start_date: str,
    end_date: str,
    purpose: str,
    session_id: Optional[str] = None,
) -> dict[str, Any]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO trips (employee_id, destination, start_date, end_date, purpose)
            VALUES (?, ?, ?, ?, ?)
            """,
            (employee_id, destination, start_date, end_date, purpose),
        )
        trip_id = cursor.lastrowid
        if session_id:
            connection.execute(
                """
                INSERT INTO session_trips (session_id, trip_id)
                VALUES (?, ?)
                ON CONFLICT(session_id) DO UPDATE SET trip_id = excluded.trip_id
                """,
                (session_id, trip_id),
            )
        trip = connection.execute(
            "SELECT id, employee_id, destination, start_date, end_date, purpose, status FROM trips WHERE id = ?",
            (trip_id,),
        ).fetchone()
    return dict(trip)


def get_trip_by_id(trip_id: int) -> Optional[dict[str, Any]]:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, employee_id, destination, start_date, end_date, purpose, status FROM trips WHERE id = ?",
            (trip_id,),
        ).fetchone()
    return dict(row) if row else None


def get_trip_for_session(session_id: str) -> Optional[dict[str, Any]]:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT t.id, t.employee_id, t.destination, t.start_date, t.end_date, t.purpose, t.status
            FROM session_trips AS st
            JOIN trips AS t ON t.id = st.trip_id
            WHERE st.session_id = ?
            """,
            (session_id,),
        ).fetchone()
    return dict(row) if row else None


def bind_trip_to_session(session_id: str, trip_id: int) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO session_trips (session_id, trip_id)
            VALUES (?, ?)
            ON CONFLICT(session_id) DO UPDATE SET trip_id = excluded.trip_id
            """,
            (session_id, trip_id),
        )
