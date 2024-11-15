from pydantic import BaseModel; 
from typing import Optional

class AddressBase(BaseModel):
    id_dirección: Optional[int] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    descripcion: Optional[str] = None
    calle: Optional[str] = None
    colonia: Optional[str] = None
    numero: Optional[int] = None
    
    class Config:
        orm_mode = True

class AddressRequest(AddressBase):
    class Config:
        orm_mode = True

class AddressResponse(AddressBase):
    id: int


    class config:
        orm_mode = True