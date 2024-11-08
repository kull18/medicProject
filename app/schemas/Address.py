from pydantic import BaseModel; 

class AddressBase(BaseModel):
    latitud: float
    longitud: float
    descripcion: str
    calle: str
    colonia: str
    numero: int
    
    class config:
        orm_mode = True

class AddressRequest(AddressBase):
    class config:
        orm_mode = True

class AddressResponse(AddressBase):
    id: int


    class config:
        orm_mode = True