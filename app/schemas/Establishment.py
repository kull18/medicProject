from pydantic import BaseModel; 


class EstablishmenBase(BaseModel):
    id_tipo_establecimiento: int
    id_dirección: int
    id_horario: int

    class config:
        orm_mode = True

class EstablishmentRequest(EstablishmenBase):
    class config:
        orm_mode = True

class EstablishmentResponse(EstablishmenBase):
    id: int


    class config:
        orm_mode = True