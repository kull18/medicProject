from pydantic import BaseModel; 
from datetime import date, time

class QuotesResponse(BaseModel):
    
    id_usuario: int
    fecha: date
    estatus: str
    horario: time
    id_doctor: int
    id_servicio: int

    class Config:
     orm_mode = True



