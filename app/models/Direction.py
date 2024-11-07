from sqlalchemy import Column, Integer, Float,String, INT, ForeignKey
from app.shared.config.db import Base

class employee(Base):
    __tablename__ = "dirección"

    id_dirección = Column(Integer, primary_key=True, autoincrement=True)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    descripcion = Column(String, nullable=True)
    calle = Column(String, nullable=True)
    colonia = Column(String, nullable=True)
    numero = Column(Integer, nullable=True)