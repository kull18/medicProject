from pydantic import BaseModel; 
from datetime import datetime

class PatientResponse(BaseModel):
    nombres: str
    contraseña: str
