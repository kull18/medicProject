from sqlalchemy import Column, Integer, Float,String, INT, ForeignKey
from app.shared.config.db import Base

class address(Base):
    __tablename__ = "dirección"

    id_dirección = Column(Integer, primary_key=True, autoincrement=True, index=True)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    descripcion = Column(String(50), nullable=True)
    calle = Column(String(50), nullable=True)
    colonia = Column(String(50), nullable=True)
    numero = Column(Integer, nullable=True)