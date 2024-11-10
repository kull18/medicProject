from sqlalchemy import Column, Integer, String, INT, ForeignKey
from app.shared.config.db import Base

class employee(Base):
    __tablename__ = "empleado"

    id_empleado = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_rol = Column(Integer, ForeignKey("rol.id_rol"),nullable = True)
    nombre = Column(String(50), nullable= True)
    contraseña = Column(String(50), nullable= True)
    id_horario = Column(Integer, ForeignKey("horario_doctores.id_horario"))
    id_establecimiento = Column(Integer, ForeignKey("establecimiento.id_establecimiento"),nullable=True)
    id_servicio = Column(Integer,ForeignKey("servicio.id_servicio") ,nullable=True)
