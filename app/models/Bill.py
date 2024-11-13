from sqlalchemy import Column, Integer, String, INT, ForeignKey
from app.shared.config.db import Base

class bills(Base):
    __tablename__ = "factura"

    folio = Column(Integer, autoincrement=True,primary_key=True,index=True)
    descripción = Column(String(100), nullable=True)
    id_cita = Column(Integer, ForeignKey("citas.id_cita"), nullable=True)
    total = Column(Integer ,nullable=True)
    comisión = Column(String(50), nullable=True)
