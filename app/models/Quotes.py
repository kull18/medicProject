from sqlalchemy import Column, Integer, String, INT, ForeignKey, TIMESTAMP, SmallInteger
from app.shared.config.db import Base

class quotes(Base):
    __tablename__ = "citas"
    
    id_cita = Column(Integer, autoincrement=True,primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("paciente.id_paciente"),nullable=True)
    fecha = Column(TIMESTAMP, nullable=True)
    estatus = Column(SmallInteger, nullable=True)
    id_servicio = Column(Integer, ForeignKey("servicio.id_servicio"),nullable=True)
