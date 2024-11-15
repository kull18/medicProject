from pydantic import BaseModel; 
from typing import Optional

class ServiceBase(BaseModel):
    id_establecimiento: Optional[int] = None
    tipo: Optional[str] = None 
    costo: Optional[int] = None

    class Config:
        orm_mode = True

class ServiceRequest(ServiceBase):
    class Config:
        orm_mode = True

class ServiceResponse(ServiceBase):
    id: int

    class Config:
        orm_mode = True