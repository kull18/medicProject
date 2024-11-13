from sqlalchemy import Column, Integer, String, INT, ForeignKey, DateTime
from app.shared.config.db import Base

class campaigns(Base):
    __tablename__ = "campañas"

    id_campañas= Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String(50), nullable=True)
    descripción = Column(String(400), nullable=True)
    dirección = Column(String(100), nullable=True)
    público = Column(String(20), nullable=True)
    fecha_inicio = Column(DateTime, nullable=True)
    id_establecimiento = Column(Integer, ForeignKey("establecimiento.id_establecimiento"),nullable=True)