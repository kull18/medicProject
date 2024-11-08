from pydantic import BaseModel; 


class PatientBase(BaseModel):
    nombres: str
    apellidos: str

    class config:
        orm_mode = True

class PatientRequest(PatientBase):
    class config:
        orm_mode = True

class PatientResponse(PatientBase):
    id: int


    class config:
        orm_mode = True