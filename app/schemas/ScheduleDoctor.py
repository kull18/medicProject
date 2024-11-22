from pydantic import BaseModel; 
from datetime import time
from typing import Optional

class ScheduleDoctorBase(BaseModel):
    id_horario: Optional[int] = None
    día: Optional[str] = None
    id_usuario: Optional[int] = None
    entrada: Optional[time] = None
    salida: Optional[time] = None
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class ScheduleDoctorRequest(ScheduleDoctorBase):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class ScheduleDoctorResponse(ScheduleDoctorBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True