from pydantic import BaseModel; 
from datetime import date, time
from typing import Optional

class QuotesResponse(BaseModel):
    
    id_usuario: int
    fecha: date
    estatus: str
    horario: time
    id_doctor: int
    id_servicio: int

    class Config:
     orm_mode = True



