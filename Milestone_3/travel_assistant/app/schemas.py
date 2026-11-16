from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class TripCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    employee_id: str = Field(min_length=1, max_length=100)
    destination: str = Field(min_length=1, max_length=200)
    start_date: date
    end_date: date
    purpose: str = Field(min_length=1, max_length=500)
    session_id: Optional[str] = Field(default=None, min_length=1, max_length=128)

    @model_validator(mode="before")
    @classmethod
    def trim_text_fields(cls, values):
        if isinstance(values, dict):
            for name in ("employee_id", "destination", "purpose", "session_id"):
                value = values.get(name)
                if isinstance(value, str):
                    values[name] = value.strip()
        return values

    @model_validator(mode="after")
    def validate_date_range(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self


class AskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(min_length=1, max_length=128)
    question: str = Field(min_length=1, max_length=2000)
    trip_id: Optional[int] = Field(default=None, gt=0)

    @model_validator(mode="before")
    @classmethod
    def trim_text_fields(cls, values):
        if isinstance(values, dict):
            for name in ("session_id", "question"):
                value = values.get(name)
                if isinstance(value, str):
                    values[name] = value.strip()
        return values
