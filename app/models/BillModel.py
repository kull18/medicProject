from pydantic import BaseModel; 

class BillsResponse(BaseModel):
    
    descripción: str
    id_cita: int
    total: int
    comisión: str
    
    class Config():
        orm_mode = True
