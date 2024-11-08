from pydantic import BaseModel; 

class BillsResponse(BaseModel):
    descripción: str
    total: int
    comisión: str
    
    class config():
        orm_mode = True
