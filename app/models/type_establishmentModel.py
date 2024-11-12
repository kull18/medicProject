from pydantic import BaseModel; 

class Type_establishmentResponse(BaseModel):
    
    tipo: str

    class Config():
        orm_mode = True
        from_attributes = True


