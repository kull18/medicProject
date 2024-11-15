from pydantic import BaseModel; 
from typing import Optional
class AddressResponse(BaseModel):
    id_dirección: Optional[int] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    descripcion: Optional[str] = None
    calle: Optional[str] = None
    colonia: Optional[str] = None
    numero: Optional[int] = None
    
    class Config():
        orm_mode = True
        arbitrary_types_allowed = True