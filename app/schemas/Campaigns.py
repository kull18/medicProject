from pydantic import BaseModel; 
from datetime import datetime

class CampaignsBase(BaseModel):

    nombre: str
    descripción: str
    dirección: str
    público: str
    fecha_inicio: datetime
    id_establecimiento: int
    

    class Config:
        orm_mode = True

class CampaignsRequest(CampaignsBase):
    class Config:
        orm_mode = True

class CampaignsResponse(CampaignsBase):
    id: int

    class Config:
        orm_mode = True