from sqlalchemy import Column, Integer, ForeignKey
from app.shared.config.db import Base

class Braiting(Base):
    __tablename__ = "puntuacion"
    
    id_puntuacion = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_establecimiento = Column(Integer, ForeignKey("establecimiento.id_establecimiento"), nullable=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=True)
    calificacion = Column(Integer, nullable=True)
