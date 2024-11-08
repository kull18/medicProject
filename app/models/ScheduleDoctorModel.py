from pydantic import BaseModel; 

class Horario(BaseModel):
    hora_inicio: str
    hora_fin: str

class ScheduleDoctorResponse(BaseModel):
    id_employee: int
    domingo: List[Horario]
    lunes: List[Horario]
    martes: List[Horario]
    miercoles: List[Horario]
    jueves: List[Horario]
    viernes: List[Horario]
    sabado: List[Horario]

    class config():
        orm_mode = True

