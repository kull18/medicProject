from pydantic import BaseModel; 
from typing import Optional

class EmployeeBase(BaseModel):
    id_rol: Optional[int] = None
    nombre: str
    contraseña: str
    id_horario: Optional[int] = None
    id_establecimiento: Optional[int] = None
    id_servicio: Optional[int] = None

    class config:
        orm_mode = True
class EmployeeLoginBase(BaseModel):
    nombre: str
    contraseña: str
    class config:
        orm_mode = True

class EmployeeRequest(EmployeeBase):
    class config:
        orm_mode = True

class EmployeeLoginReques(EmployeeLoginBase):
    class config:
        orm_mode = True

class EmployeeResponse(EmployeeBase):
    id: int

    class config:
        orm_mode = True