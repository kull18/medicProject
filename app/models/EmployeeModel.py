from pydantic import BaseModel
from typing import Optional

class EmployeeResponse(BaseModel):
    id_rol: Optional[int] = None
    nombre: str
    contraseña: str
    id_horario: Optional[int] = None
    id_establecimiento: Optional[int] = None
    id_servicio: Optional[int] = None
    
    class Config:
        orm_mode = True
