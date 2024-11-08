from pydantic import BaseModel; 

class CampaignsBase(BaseModel):
    nombre: str
    descripción: str
    id_establecimiento: int

    class config:
        orm_mode = True

class CampaignsRequest(CampaignsBase):
    class config:
        orm_mode = True

class CampaignsResponse(CampaignsBase):
    id: int


    class config:
        orm_mode = True