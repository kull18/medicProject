from sqlalchemy import Column, Integer, String, INT, ForeignKey, TIMESTAMP, SmallInteger
from app.shared.config.db import Base

class patient(Base):
    __tablename__ = "paciente"
    
    id_paciente = Column(Integer,primary_key=True, autoincrement=True, index=True)
    nombres = Column(String(50), nullable=True)
    apellidos = Column(String(50), nullable=True)