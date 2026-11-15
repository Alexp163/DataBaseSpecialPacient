from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PatientCreateSchema(BaseModel):
    last_name: str = Field(min_length=1, max_length=100)
    first_name: str = Field(min_length=1, max_length=100)
    middle_name: str | None = None
    date_birth: date
    card_number: str = Field(min_length=1, max_length=50)
    rating: float = Field(default=0.0, ge=0, le=10)
    positive: str | None = None
    negativity: str | None = None
    attention: str | None = None

    @field_validator("date_birth")
    @classmethod
    def date_birth_not_in_future(cls, v: date) -> date | None:
        if v is not None and v > date.today():
            raise ValueError("date_birth не может быть в будущем")
        return v


class PatientReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_name: str
    first_name: str
    middle_name: str | None = None
    date_birth: date
    card_number: str
    rating: float
    positive: str | None = None
    negativity: str | None = None
    attention: str | None = None
    created_at: datetime
    updated_at: datetime


class PatientUpdateSchema(BaseModel):
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    middle_name: str | None = Field(default=None, max_length=100)
    date_birth: date | None = None
    card_number: str | None = Field(default=None, min_length=1, max_length=50)
    rating: float | None = Field(default=None, ge=0, le=10)
    positive: str | None = None
    negativity: str | None = None
    attention: str | None = None

    @field_validator("date_birth")
    @classmethod
    def date_birth_not_in_future(cls, v: date | None) -> date | None:
        if v is not None and v > date.today():
            raise ValueError("date_birth не может быть в будущем")
        return v
