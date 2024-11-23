from pydantic import BaseModel; 
from typing import Optional 

class BraitingBase(BaseModel):
    id_puntuacion: Optional[int] = None
    id_establecimiento: Optional[int] = None
    id_usuario:  Optional[int] = None
    calificacion: Optional[int] = None 
    
    class Config:
        orm_mode = True

class BraitingRequest(BraitingBase):
    class Config:
        orm_mode = True

class BraitingResponse(BraitingBase):
    id_puntuacion: int  

    class Config:
        orm_mode = True
        from_attributes=True
