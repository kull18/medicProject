from pydantic import BaseModel; 
from datetime import date

class QuotesBase(BaseModel):
    id_usuario: int
    fecha: date
    estatus: int 
    id_servicio: int

    class Config:
        orm_mode = True

class QuotesRequest(QuotesBase):
    class Config:
        orm_mode = True

class QuotesResponse(QuotesBase):
    id: int
    
    class Config:
        orm_mode = True