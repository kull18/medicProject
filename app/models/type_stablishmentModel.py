from pydantic import BaseModel; 

class Type_establishmentResponse(BaseModel):
    tipo: str


    class config():
        orm_mode = True

