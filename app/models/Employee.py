from sqlalchemy import Column, Integer, String, INT, ForeignKey
from app.shared.config.db import Base

class employee(Base):
    __tablename__ = "empleado"

    id_empleado = Column(Integer, primary_key=True, autoincrement=True)
    id_rol = Column(Integer, ForeignKey("rol.id_rol"),nullable = True)
    nombre = Column(String, nullable= True)
    contraseña = Column(String, nullable= True)
    horario = Column(Integer, nullable=True)
    id_establecimiento = Column(Integer, ForeignKey("establecimiento.id_establecimiento"),nullable=True)
    id_servicio = Column(Integer,ForeignKey("servicio.id_servicio") ,nullable=True)
