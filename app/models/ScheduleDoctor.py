from sqlalchemy import Column, Integer, ForeignKey,String, INT, Time
from app.shared.config.db import Base


class ScheduleDoctor(Base):
    __tablename__ = "horario_doctores"

    id_horario = Column(Integer,autoincrement=True,primary_key=True,index=True)
    día = Column(String(10), nullable=True)
    entrada = Column(Time, nullable=True); 
    salida = Column(Time,nullable=True); 
