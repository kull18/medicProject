from pydantic import BaseModel; 


class EmployeeBase(BaseModel):
    id_rol: int
    nombre: str
    contraseña: str
    id_horario: int
    id_establecimiento: int
    id_servicio: int
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