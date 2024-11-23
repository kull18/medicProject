from pydantic import BaseModel; 
from typing import Optional

class UserBase(BaseModel):
    id_usuario: Optional[int] = None
    id_rol: Optional[int] = None
    nombre: Optional[str] = None
    contraseña: Optional[str] = None
    localidad: Optional[str] = None
    id_establecimiento: Optional[int] = None
    id_servicio: Optional[int] = None

    class Config:
        orm_mode = True


class UserLoginBase(BaseModel):
    nombre: str
    contraseña: str
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class UserRequest(UserBase):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class UserLoginReques(UserLoginBase):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True