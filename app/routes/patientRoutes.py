from fastapi import APIRouter, Form, Depends; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.config.db import get_db, Base
import app.models
from app.schemas.TokenModel import Token
from app.models.Patient import patient
from app.services.authService import loguearseUser
from app.services.employeeService import createUserNormal
from app.schemas.Patient import PatientLoginRequest
from app.schemas.Patient import PatientRequest, PatientResponse
from app.models.PatientModel import PatientResponse


patientRoutes = APIRouter(
    tags=["patient"],
    deprecated=False
); 


@patientRoutes.post('/patient/', status_code=status.HTTP_201_CREATED, response_model=PatientResponse)
async def create_patient(post_patient: PatientRequest, db: Session = Depends(get_db)):
    new_patient = createUserNormal(db=db, patient_data=post_patient)
    return new_patient

@patientRoutes.get('/patient/', status_code= status.HTTP_200_OK, response_model= List[PatientResponse])
async def get_patients(db: Session = Depends(get_db)):
    all_patients = db.query(patient).all(); 
    for i in all_patients:
        print("establishment")
    return all_patients; 


@patientRoutes.post("/loginPatient", response_model=Token)
async def login_employee(user: PatientLoginRequest,db: Session = Depends(get_db)):
    try:
        userFind = loguearseUser(Patient=user, db=db); 
        return Token(access_token=userFind)
    except Exception as e:
        return e; 

@patientRoutes.put("/patient/{id_patient}", response_model=PatientResponse)
async def change_patient(id_patient: int, employeeChange:PatientRequest,db: Session = Depends(get_db)): 
    change_patient = db.query(patient).filter(patient.id_paciente == id_patient).first()
    if change_patient is None:
        raise HTTPException(
            status_code=404,
            detail="patient no encontrado"
        )
    
    for key, value in employeeChange.dict().items():
        setattr(
            change_patient, 
            key, value
        )
    
    db.commit()
    db.refresh(change_patient)
    return change_patient

@patientRoutes.delete("/patient/{id_patient}", response_model=PatientResponse)
async def delete_patient(id_patient: int, db: Session = Depends(get_db)):
    delete_patient = db.query(patient).filter(patient.id_paciente == id_patient).first()
    if delete_patient is None:
        raise HTTPException(
            status_code=404, 
            detail="patient no encontrado"
        )
    
    db.delete(delete_patient)
    db.commit()
    return delete_patient
    