from pydantic import BaseModel; 


class Type_establishmentBase(BaseModel):
    tipo: str

    class config:
        orm_mode = True

class Type_establishmentRequest(Type_establishmentBase):
    class config:
        orm_mode = True

class Type_establishmentResponse(Type_establishmentBase):
    id: int


    class config:
        orm_mode = True