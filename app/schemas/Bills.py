from pydantic import BaseModel; 

class BillsBase(BaseModel):
    
    descripción: str
    total: int
    comisión: str
    
    class Config:
        orm_mode = True

class BillsRequest(BillsBase):
    class Config:
        orm_mode = True

class BillsResponse(BillsBase):
    id: int

    class Config:
        orm_mode = True