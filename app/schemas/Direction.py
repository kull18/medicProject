from pydantic import BaseModel; 

class DirectionBase(BaseModel):
    id_establecimiento: int
    id_tipo_establecimiento : int
    id_dirección: int
    id_horario: int

    class config:
        orm_mode = True

class DirectionRequest(DirectionBase):
    class config:
        orm_mode = True

class DirectionResponse(DirectionBase):
    id: int


    class config:
        orm_mode = True