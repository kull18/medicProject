from sqlalchemy import Column, Integer, ForeignKey,String, INT
from app.shared.config.db import Base


class Service(Base):
    __tablename__ = "servicio"

    id_servicio = Column(Integer, primary_key=True)
    id_establecimiento = Column(Integer, ForeignKey("establicimiento.id_establecimiento"),nullable=True)
    tipo = Column(String, nullable=True)
    costo = Column(Integer, nullable=True)
    serviciocol = Column(String, nullable=True)