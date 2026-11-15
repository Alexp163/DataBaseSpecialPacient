from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from datetime import date
from fastapi.responses import RedirectResponse
from sqlalchemy import insert, select, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from patients.models import Patient
from patients.schemas import PatientCreateSchema, PatientReadSchema, PatientUpdateSchema

router = APIRouter(tags=["patient"], prefix="/patients")


@router.post("/", status_code=status.HTTP_303_SEE_OTHER)  # 1) Создание пациента
async def create_patient(
    request: Request,
    patient: PatientCreateSchema,
    session: AsyncSession = Depends(get_async_session),
):
    statement = insert(Patient).values(**patient.model_dump()).returning(Patient)
    try:
        await session.scalar(statement)
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        if "ix_patient_card_number" in str(exc.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пациент с таким номером карты уже существует",
            ) from exc
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось сохранить пациента",
        ) from exc

    return RedirectResponse(
        url="/patient/success", status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/", status_code=status.HTTP_200_OK)  # 2) получает данные о всех пациентах
async def get_users(session=Depends(get_async_session)) -> list[PatientReadSchema]:
    statement = select(Patient)
    result = await session.scalars(statement)
    return list(result)


@router.get("/search", response_model=list[PatientReadSchema]) # 3) Поиск пациента в базе данных
async def search_patients(
    last_name: str | None = Query(None, max_length=100, description="Фамилия"),
    first_name: str | None = Query(None, max_length=100, description="Имя"),
    middle_name: str | None = Query(None, max_length=100, description="Отчество"),
    date_birth: date | None = Query(None, description="Дата рождения"),
    card_number: str | None = Query(None, max_length=50, description="Номер мед.какрты"),
    session: AsyncSession = Depends(get_async_session)
) -> list[PatientReadSchema]:
    if not any([last_name, first_name, middle_name, date_birth, card_number]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Укажите хотя бы один параметр поиска",
        )
    patients_query = select(Patient)

    if last_name:
        patients_query = patients_query.where(Patient.lastname.ilike(f"%{last_name.strip()}%"))
    if first_name:
        patients_query = patients_query.where(Patient.first_name.ilike(f"%{first_name.strip()}%"))
    if middle_name:
        patients_query = patients_query.where(Patient.middle_name.ilike(f"%{middle_name.strip()}%"))
    if date_birth:
        patients_query = patients_query.where(Patient.middle_name.ilike(f"%{date_birth.strip()}%"))
    if card_number:
        patients_query = patients_query.where(Patient.middle_name.ilike(f"%{card_number.strip()}%"))

    result = await session.scalars(
        patients_query.order_by(Patient.last_name, Patient.first_name)
    )
    return list(result.all())


@router.get("/{patient_id}", status_code=status.HTTP_200_OK)  # 4) Найти пациента по id
async def get_patient_by_id(patient_id: int, session: AsyncSession = Depends(get_async_session)) -> PatientReadSchema:
    statement = select(Patient).where(Patient.id == patient_id)
    result = await session.scalar(statement)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пациент не найден",
        )
    return result 


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)  # 5) Удалить пациента по id
async def delete_patient(
    patient_id: int, 
    session: AsyncSession = Depends(get_async_session),
) -> None:
    statement = delete(Patient).where(Patient.id == patient_id)
    result = await session.execute(statement)
    await session.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пациент не найден"
        )


@router.patch("/{patient_id}", status_code=status.HTTP_200_OK)  # 6) Обновить пациента по id 
async def upgrade_patient_by_id(patient_id: int, patient: PatientUpdateSchema,
                                session: AsyncSession=Depends(get_async_session)) -> PatientReadSchema:
    statement = update(Patient).where(Patient.id == patient_id).values(
        last_name=patient.last_name,
        first_name=patient.first_name,
        middle_name=patient.middle_name,
        date_birth=patient.date_birth,
        card_number=patient.card_number,
        rating=patient.rating,
        positive=patient.positive,
        negativity=patient.negativity,
        attention=patient.attention,
    ).returning(Patient)
    result = await session.scalar(statement)
    if result is None:
        raise HTTPException(status_code=404, detail="Пациент не найден")
    await session.commit()
    return result 




    