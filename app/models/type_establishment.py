from sqlalchemy import Column, Integer, ForeignKey,String, INT
from app.shared.config.db import Base


class TypeEstablishment(Base):
    __tablename__ = "tipo_establecimiento"

    id_tipo_establecimiento = Column(Integer, autoincrement=True,primary_key=True, index=True)
    tipo = Column(String(20), nullable=True)