from pydantic import BaseModel; 

class BillsBase(BaseModel):
    descripción: str
    total: int
    comisión: str
    
    class config:
        orm_mode = True

class BillsRequest(BillsBase):
    class config:
        orm_mode = True

class BillsResponse(BillsBase):
    id: int


    class config:
        orm_mode = True