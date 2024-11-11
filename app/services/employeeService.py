from sqlalchemy.orm import Session
from app.schemas.Employee import EmployeeRequest
from app.schemas.Patient import PatientRequest
from app.models.Employee import employee
from app.models.Patient import patient
from app.shared.utils.security import hash_password
from fastapi import HTTPException


def createUser(db: Session, employee_data: EmployeeRequest):
    try:
        hashed_password = hash_password(employee_data.contraseña)
        
        db_user = employee(
            id_rol=employee_data.id_rol,
            nombre=employee_data.nombre,
            contraseña=hashed_password,
            id_horario=employee_data.id_horario,
            id_establecimiento=employee_data.id_establecimiento,
            id_servicio=employee_data.id_servicio
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear el usuario: {str(e)}")
    

def createUserNormal(db: Session, patient_data: PatientRequest):
    try:
        hashed_password = hash_password(patient_data.contraseña)
        
        db_user = patient(
            nombres = patient_data.nombres,
            apellidos = patient_data.apellidos,
            contraseña = hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear el patient : {str(e)}")


def getUsers(db:Session):
    datos =   db.query(employee).all()
    return datos