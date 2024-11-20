from pydantic import BaseModel; 

class Type_establishmentResponse(BaseModel):
    id_tipo_establecimiento: int
    tipo: str

    class Config():
        orm_mode = True
        from_attributes = True


