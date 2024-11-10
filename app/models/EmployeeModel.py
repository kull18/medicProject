from pydantic import BaseModel; 

class EmployeeResponse(BaseModel):
    id_rol: int
    nombre: str
    contraseña: str
    id_horario: int
    id_establecimiento: int
    id_servicio: int
    
    class config():
        orm_mode = True

