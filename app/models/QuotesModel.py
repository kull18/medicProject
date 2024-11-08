from pydantic import BaseModel; 
from datetime import datetime

class QuotesResponse(BaseModel):
    id_paciente: int
    fecha: datetime
    estatus: int 
    id_servicio: int

class config:
    orm_mode = True
