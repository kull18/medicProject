from sqlalchemy import Column, Integer, Time,ForeignKey,String, INT
from app.shared.config.db import Base


class Schedule(Base):
    __tablename__ = "horario"

    id_horario = Column(Integer,autoincrement=True,primary_key=True,index=True)
    entrada = Column(Time, nullable=True); 
    salida = Column(Time,nullable=True); 