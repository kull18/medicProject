from sqlalchemy import Column, Integer, String, INT, ForeignKey, TIMESTAMP, SmallInteger
from app.shared.config.db import Base

class patient(Base):
    __tablename__ = "paciente"
    
    id_paciente = Column(Integer, autoincrement=True,primary_key=True, index=True)
    nombres = Column(String(), nullable=True)
    contraseñas = Column(String(), nullable=True)