from pydantic import BaseModel; 
from typing import Optional
class ServiceResponse(BaseModel):
    
    id_establecimiento: Optional[int] = None
    tipo: Optional[str] = None
    costo: Optional[int] = None
    
    class Config():
        orm_mode = True
        from_attributes = True


