from pydantic import BaseModel; 

class EstablishmentResponse(BaseModel):
    id_tipo_establecimiento: int
    id_dirección: int
    hora_apertura: time
    hora cierre: time

    class config():
        orm_mode = True

