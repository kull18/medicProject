from pydantic import BaseModel; 

class ServiceResponse(BaseModel):
    
    id_establecimiento: int
    tipo: str
    costo: int
    
    class Config():
        orm_mode = True
        from_attributes = True


