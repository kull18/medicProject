from pydantic import BaseModel; 
from datetime import time
from typing import Optional

class ScheduleDoctorBase(BaseModel):
    día: Optional[str]
    entrada: Optional[time]
    salida: Optional[time]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class ScheduleDoctorRequest(ScheduleDoctorBase):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class ScheduleDoctorResponse(ScheduleDoctorBase):
    id: int

    class Config:
        orm_mode = True