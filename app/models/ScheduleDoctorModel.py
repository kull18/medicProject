from pydantic import BaseModel; 
from datetime import time
from typing import Optional
class ScheduleDoctorResponse(BaseModel):
    día: Optional[str] = None
    id_usuario: Optional[int] = None
    entrada: Optional[time] = None
    salida: Optional[time] = None

    class Config:
        orm_mode = True
        from_attributes = True