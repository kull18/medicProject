from pydantic import BaseModel; 
from datetime import date

class QuotesResponse(BaseModel):
    
    id_usuario: int
    fecha: date
    estatus: int 
    id_servicio: int

    class Config:
     orm_mode = True



