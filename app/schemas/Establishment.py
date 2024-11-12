from pydantic import BaseModel; 
from typing import List, Optional

class EstablishmenBase(BaseModel):
    id_tipo_establecimiento: Optional[int] = None
    id_dirección: Optional[int] = None
    id_horario: Optional[int] = None
    nombre: Optional[str] = None

    class Config:
        orm_mode = True

class EstablishmentRequest(EstablishmenBase):
    class Config:
        orm_mode = True

class EstablishmentResponse(EstablishmenBase):
    id: int


    class config:
        orm_mode = True
