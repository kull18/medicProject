from pydantic import BaseModel; 
from time import time

class ScheduleDoctorBase(BaseModel):
    día: str
    entrada: str 
    salida: str

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