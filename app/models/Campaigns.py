from sqlalchemy import Column, Integer, String, INT, ForeignKey
from app.shared.config.db import Base

class campaigns(Base):
    __tablename__ = "campañas"

    id_campañas= Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String(50), nullable=True)
    descripción = Column(String(400), nullable=True)
    id_establecimiento = Column(Integer, ForeignKey("establecimiento.id_establecimiento"),nullable=True)