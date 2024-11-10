from sqlalchemy import Column, Integer, String, INT, ForeignKey
from app.shared.config.db import Base


class Establishment(Base):
    __tablename__ = "establecimiento"

    id_establecimiento = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_tipo_establecimiento = Column(Integer, ForeignKey("tipo_establecimiento.id_tipo_establecimiento"), nullable=True)
    id_dirección = Column(Integer, ForeignKey("dirección.id_dirección"),nullable=True)
    hora_apertura = Column(Time, nullable=True)
    hora_cierre = Column(Time, nullable=True)