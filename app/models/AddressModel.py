from pydantic import BaseModel; 

class AddressResponse(BaseModel):
    id_dirección: int
    latitud: float
    longitud: float
    descripcion: str
    calle: str
    colonia: str
    numero: int
    
    
    class config():
        orm_mode = True