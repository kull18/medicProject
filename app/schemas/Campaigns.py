from pydantic import BaseModel; 
from datetime import datetime
from typing import Optional

class CampaignsBase(BaseModel):
    id_campañas: Optional[int] = None
    nombre: Optional[str] = None
    descripción: Optional[str] = None
    dirección: Optional[str] = None
    público: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    id_establecimiento: Optional[int] = None
    

    class Config:
        orm_mode = True

class CampaignsRequest(CampaignsBase):
    class Config:
        orm_mode = True

class CampaignsResponse(CampaignsBase):
    id: int

    class Config:
        orm_mode = True