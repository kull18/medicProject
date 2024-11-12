from pydantic import BaseModel; 

class ServiceResponse(BaseModel):
    
    id_establecimiento: int
    tipo: str
    costo: int
    serviciocol: str

    class Config():
        orm_mode = True
        from_attributes = True


