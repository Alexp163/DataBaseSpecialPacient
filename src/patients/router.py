from fastapi import APIRouter, Depends, status 
from sqlalchemy import delete, insert, select, update 
from schemas import PatientCreateSchema, PatientReadSchema, PatientUpdateSchema
from database import get_async_session
from models import Patient
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["patient"], prefix="/patient")

@router.post("/", status_code=status.HTTP_201_CREATED) # 1) Создание пациента
async def create_patient(patient: PatientCreateSchema, 
                         session: AsyncSession=Depends(get_async_session)) -> PatientReadSchema:
    statement = insert(Patient).values(
        name=patient.name,
        date_birth=patient.date_birth,
        card_number=patient.card_number,
        rating=patient.rating,
        positive=patient.positive,
        negativity=patient.negativity,
        attention=patient.attention
    ).returning(Patient)
    result = await session.scalar(statement)
    await session.commit()
    return result 




