from pydantic import BaseModel; 
from datetime import time
class ScheduleResponse(BaseModel):
    
    entrada: time
    salida: time
    
    class Config():
        orm_mode = True
        arbitrary_types_allowed = True

