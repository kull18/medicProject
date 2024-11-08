from pydantic import BaseModel; 

class ScheduleResponse(BaseModel):
    id_establecimiento: int
    tipo: str
    costo: int
    serviciocol: str

    class config():
        orm_mode = True

