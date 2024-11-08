from sqlalchemy import Column, Integer, ForeignKey,String, INT
from app.shared.config.db import Base


class Service(Base):
    __tablename__ = "horario de doctores"

    id_horario_doctor = Column(Integer, autoincrement=True,primary_key=True, index=True)
    aquí no sé cómo hacerle