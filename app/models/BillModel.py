from pydantic import BaseModel; 

class BillsResponse(BaseModel):
    
    descripción: str
    total: int
    comisión: str
    
    class Config():
        orm_mode = True
