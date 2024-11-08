from pydantic import BaseModel; 
from datetime import datetime

class QuotesBase(BaseModel):
    id_paciente: int
    fecha: datetime
    estatus: int 
    id_servicio: int

    class config:
        orm_mode = True

class QuotesRequest(QuotesBase):
    class config:
        orm_mode = True

class QuotesResponse(QuotesBase):
    id: int


    class config:
        orm_mode = True