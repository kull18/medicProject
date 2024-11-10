from pydantic import BaseModel; 

class EstablishmentResponse(BaseModel):
    id_tipo_establecimiento: int
    id_dirección: int
    id_horario: int

    class config():
        orm_mode = True

