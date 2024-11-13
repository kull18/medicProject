from pydantic import BaseModel; 
from datetime import datetime

class CampaignsResponse(BaseModel):
    
    nombre: str
    descripción: str
    dirección: str
    público: str
    fecha_inicio: datetime
    id_establecimiento: int
    
    class Config():
        orm_mode = True
