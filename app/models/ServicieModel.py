from pydantic import BaseModel; 

class ServiceResponse(BaseModel):
    id_establecimiento: int
    tipo: str
    costo: int
    serviciocol: str

    class config():
        orm_mode = True

