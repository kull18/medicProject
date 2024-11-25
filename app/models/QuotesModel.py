from pydantic import BaseModel; 
from datetime import date, time
from typing import Optional

class QuotesResponse(BaseModel):
    id_cita: Optional[int] = None
    id_usuario: Optional[int] = None
    fecha: Optional[date] = None
    horario: Optional[time] = None
    estatus: Optional[str] = None
    id_doctor: Optional[int] = None
    id_servicio: Optional[int] = None 

    class Config:
     orm_mode = True



