from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, DateTime, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from database import Base


class Patient(Base):
    __tablename__ = "patient"
    __table_args__ = (
        CheckConstraint("rating >= 0 AND rating <= 10", name="ck_patient_rating_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )  # Ф.И.О. пациента
    date_birth: Mapped[date] = mapped_column(Date, nullable=False)  # дата рождения

    card_number: Mapped[str] = mapped_column(  # номер медицинской карты
        String(50), nullable=False, unique=True, index=True
    )

    rating: Mapped[float] = mapped_column(  # рейтинг пациента
        Float, nullable=False, default=0.0, server_default="0"
    )

    positive: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # позитивные стороны
    negativity: Mapped[str | None] = mapped_column(Text, nullable=True)  # негатив
    attention: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # обрати внимание

    created_at: Mapped[datetime] = mapped_column(  # дата создания
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(  # дата обновления
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Patient id={self.id} name={self.name!r} card_number={self.card_number!r}>"
