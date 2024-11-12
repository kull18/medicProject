from pydantic import BaseModel; 


class Type_establishmentBase(BaseModel):
    tipo: str

    class Config:
        orm_mode = True

class Type_establishmentRequest(Type_establishmentBase):
    class Config:
        orm_mode = True

class Type_establishmentResponse(Type_establishmentBase):
    id: int
    
    class Config:
        orm_mode = True