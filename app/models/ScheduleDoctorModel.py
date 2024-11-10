from pydantic import BaseModel; 

class ScheduleDoctorResponse(BaseModel):
    día: str
    entrada: str 
    salida: str

    class config():
        orm_mode = True

