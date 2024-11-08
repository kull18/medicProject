from pydantic import BaseModel; 

class CampaignsResponse(BaseModel):
    nombre: str
    descripción: str
    id_establecimiento: int
    
    class config():
        orm_mode = True
