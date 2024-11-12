from pydantic import BaseModel; 
from datetime import time
from typing import Optional
class ScheduleDoctorResponse(BaseModel):
    
    día: Optional[str]
    entrada: Optional[time] 
    salida: Optional[time]

    class Config():
        orm_mode = True

