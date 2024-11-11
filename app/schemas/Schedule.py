from pydantic import BaseModel; 
from datetime import time

class ScheduleBase(BaseModel):
    entrada: time
    salida: time
    
    class config:
        orm_mode = True
        arbitrary_types_allowed = True

class ScheduleRequest(ScheduleBase):
    class config:
        orm_mode = True
        arbitrary_types_allowed = True

class ScheduleResponse(ScheduleBase):
    id: int


    class config:
        orm_mode = True