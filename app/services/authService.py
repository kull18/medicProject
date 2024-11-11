from sqlalchemy.orm import Session
from app.schemas.Employee import EmployeeLoginReques
from app.models.Employee import employee
from app.models.Patient import patient
from fastapi import HTTPException, status
from app.shared.utils.security import verify_password
from app.shared.middlewares.generateToken import generateToken
from app.schemas.Patient import PatientLoginRequest

def loguearse(Employee: EmployeeLoginReques, db: Session):
    db_user = db.query(employee).filter(employee.nombre == Employee.nombre).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El empleado no está registrado"
        )
    
    if not verify_password(Employee.contraseña, db_user.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta"
        )
    
    access_token = generateToken(data={"correo": db_user.nombre, "id_rol": db_user.id_rol})
    return access_token; 

def loguearseUser(Patient: PatientLoginRequest, db: Session):
    db_user = db.query(patient).filter(patient.nombres == Patient.nombres).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El paciente no está registrado"
        )
    
    if not verify_password(Patient.contraseña, db_user.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta"
        )
    
    access_token = generateToken(data={"nombre": db_user.nombres, "id_role": db_user.id_paciente})
    return access_token; 