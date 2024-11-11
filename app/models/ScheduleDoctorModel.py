from pydantic import BaseModel; 
from datetime import time
class ScheduleDoctorResponse(BaseModel):
    día: str
    entrada: time 
    salida: time

    class config():
        orm_mode = True

