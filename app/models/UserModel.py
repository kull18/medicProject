from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    id_usuario: Optional[int] = None
    id_rol: int
    nombre: str
    contraseña: str
    id_establecimiento: Optional[int] = None
    id_servicio: Optional[int] = None

    class Config:
        orm_mode = True
        from_attributes = True