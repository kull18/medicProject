from pydantic import BaseModel; 


class ServiceBase(BaseModel):
    id_establecimiento: int
    tipo: str
    costo: int
    serviciocol: str

    class Config:
        orm_mode = True

class ServiceRequest(ServiceBase):
    class Config:
        orm_mode = True

class ServiceResponse(ServiceBase):
    id: int

    class Config:
        orm_mode = True