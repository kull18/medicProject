from pydantic import BaseModel; 
from typing import Optional
class BraitingModel(BaseModel):
    id_puntuacion: Optional[int] = None
    id_establecimiento: Optional[int] = None
    id_usuario: Optional[int] = None
    calificacion: Optional[int] = None

    class Config():
        orm_mode = True
        arbitrary_types_allowed = True