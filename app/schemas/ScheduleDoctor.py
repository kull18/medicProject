from pydantic import BaseModel; 
from datetime import time

class ScheduleDoctorBase(BaseModel):
    día: str
    entrada: time 
    salida: time

    class config:
        orm_mode = True
        arbitrary_types_allowed = True

class ScheduleDoctorRequest(ScheduleDoctorBase):
    class config:
        orm_mode = True
        arbitrary_types_allowed = True

class ScheduleDoctorResponse(ScheduleDoctorBase):
    id: int


    class config:
        orm_mode = True