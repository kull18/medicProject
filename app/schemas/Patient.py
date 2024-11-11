from pydantic import BaseModel; 


class PatientBase(BaseModel):
    nombres: str
    apellidos: str
    contraseña: str

    class config:
        orm_mode = True

class PatientRequest(PatientBase):
    class config:
        orm_mode = True



class PatientLoginBase(BaseModel):
    nombres: str
    contraseña: str

    class config:
        orm_mode = True

class PatientLoginRequest(PatientLoginBase):
    class config:
        orm_mode = True



class PatientResponse(PatientBase):
    id: int


    class config:
        orm_mode = True