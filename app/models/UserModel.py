from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    id_usuario: Optional[int] = None
    id_rol: Optional[int] = None
    nombre: Optional[str] = None
    contraseña: Optional[str] = None
    id_establecimiento: Optional[int] = None
    localidad: Optional[str] = None
    id_servicio: Optional[int] = None

    class Config:
        orm_mode = True
        from_attributes = True