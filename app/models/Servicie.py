from sqlalchemy import Column, Integer, ForeignKey,String, INT
from app.shared.config.db import Base

class Service(Base):
    __tablename__ = "servicio"

    id_servicio = Column(Integer, autoincrement=True,primary_key=True, index=True)
    id_establecimiento = Column(Integer, ForeignKey("establecimiento.id_establecimiento"),nullable=True)
    tipo = Column(String(20), nullable=True)
    costo = Column(Integer, nullable=True)
    serviciocol = Column(String(50), nullable=True)


