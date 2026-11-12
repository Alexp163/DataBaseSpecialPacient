from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func 
from datetime import datetime 



class Patient(Base):
    __tablename__ = "patient"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()  # Ф.И.О. пациента
    date_birth: Mapped[datetime] = mapped_column(server_default=func.now())  # дата рождения
    card_number: Mapped[str] = mapped_column()  # номер медицинской карты
    rating: Mapped[float] = mapped_column()  # райтинг пациента
    positive: Mapped[str] = mapped_column()  # позитивные стороны
    negativity: Mapped[str] = mapped_column()  # негатив
    attention: Mapped[str] = mapped_column()  # обрати внимание
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())  # дата создания
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )  # дата обновления

    def __repr__(self):
        return f"{self.name} {self.date_birth} {self.card_number} {self.rating} {self.positive} {self.negativity} {self.attention}"


    