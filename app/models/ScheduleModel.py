from pydantic import BaseModel; 
from datetime import time
from typing import Optional
class ScheduleResponse(BaseModel):
    id_horario: Optional[int] = None
    entrada: Optional[time] = None
    salida: Optional[time] = None
    
    class Config():
        orm_mode = True
        arbitrary_types_allowed = True

