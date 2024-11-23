from sqlalchemy import Column, Integer, String, INT, ForeignKey, Time
from app.shared.config.db import Base
from sqlalchemy.orm import relationship

class Establishment(Base):
    __tablename__ = "establecimiento"

    id_establecimiento = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_tipo_establecimiento = Column(Integer, ForeignKey("tipo_establecimiento.id_tipo_establecimiento"), nullable=True)
    descripción = Column(String(255), nullable=True)
    localidad = Column(String(200), nullable=True)
    categoria = Column(String(50), nullable=True)
    id_dirección = Column(Integer, ForeignKey("dirección.id_dirección"),nullable=True)
    id_horario = Column(Integer, ForeignKey("horario.id_horario"), nullable=True)   
    nombre = Column(String(100), nullable=True)




