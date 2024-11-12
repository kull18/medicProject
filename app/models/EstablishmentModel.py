from pydantic import BaseModel
from typing import Optional
class EstablishmentResponse(BaseModel):

    id_tipo_establecimiento: Optional[int] = None
    id_dirección: Optional[int] = None  
    id_horario: Optional[int] = None
    nombre: Optional[str] = None
    
    class Config():
        orm_mode = True
        from_attributes = True



