from pydantic import BaseModel; 
from datetime import time
from typing import Optional

class ScheduleBase(BaseModel):
    id_horario: Optional[int] = None
    entrada: Optional[time] = None
    salida: Optional[time] = None
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class ScheduleRequest(ScheduleBase):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class ScheduleResponse(ScheduleBase):
    id: int

    class Config:
        orm_mode = True