from pydantic import BaseModel; 
from datetime import date

class QuotesResponse(BaseModel):
    id_paciente: int
    fecha: date
    estatus: int 
    id_servicio: int

class config:
    orm_mode = True
