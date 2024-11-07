from pydantic import BaseModel; 


class ServiceBase(BaseModel):
    id_servicio: int
    id_establecimiento: int
    tipo: str
    costo: int
    serviciocol: str

    class config:
        orm_mode = True

class ServiceRequest(ServiceBase):
    class config:
        orm_mode = True

class ServiceResponse(ServiceBase):
    id: int


    class config:
        orm_mode = True