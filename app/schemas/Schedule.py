from pydantic import BaseModel; 
from datetime import time

class ScheduleBase(BaseModel):
    entrada: time
    salida: time
    
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