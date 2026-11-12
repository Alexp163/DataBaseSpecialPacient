from pydantic import BaseModel, ConfigDict
from datetime import datetime, date 


class PatientCreateSchema(BaseModel):
    name: str
    date_birth: date 
    card_number: str 
    rating: float 
    positive: str | None = None
    negativity: str |None = None 
    attention: str | None = None 


class PatientReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    date_birth: date 
    card_number: str 
    rating: float 
    positive: str | None = None
    negativity: str |None = None 
    attention: str | None = None 
    created_at: datetime
    updated_at: datetime


class PatientUpdateSchema(BaseModel):
    name: str | None = None
    date_birth: date | None = None
    card_number: str | None = None
    rating: float | None = None
    positive: str | None = None
    negativity: str |None = None 
    attention: str | None = None 

