from sqlalchemy import Column, Integer, ForeignKey,String, INT
from app.shared.config.db import Base


class Service(Base):
    __tablename__ = "horario"

    id_horario = Column(Integer, autoincrement=True,primary_key=True, index=True)
    entrada = Column(); 
    salida = Column(); 