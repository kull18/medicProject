from pydantic import BaseModel; 
from time import time
class ScheduleResponse(BaseModel):
    entrada: str
    salida: str 
    
    class config():
        orm_mode = True
        arbitrary_types_allowed = True

