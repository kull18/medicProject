from fastapi import APIRouter, Form, Depends; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.config.db import get_db, Base
import app.models
from app.models.Establishment import Establishment
from app.schemas.Establishment import EstablishmentRequest, EstablishmentResponse
from app.models.EstablishmentModel import EstablishmentResponse
establishmentRoutes = APIRouter(); 


@establishmentRoutes.post('/establishment/', status_code=status.HTTP_201_CREATED, response_model=EstablishmentResponse)
async def create_employee(post_employee: EstablishmentRequest, db: Session = Depends(get_db)):
    new_establishment = Establishment(**post_employee.model_dump())
    db.add(new_establishment)
    db.commit()
    db.refresh(new_establishment)
    return new_establishment.__dict__


@establishmentRoutes.get('/establishment/', status_code= status.HTTP_200_OK, response_model= List[EstablishmentResponse])
async def get_employees(db: Session = Depends(get_db)):
    all_establishments = db.query(Establishment).all(); 
    for i in all_establishments:
        print("establishment")
    return all_establishments; 


@establishmentRoutes.put("/establishment/${id_establishment}", response_model=EstablishmentResponse)
async def change_establishment(id_establishment: int, employeeChange: EstablishmentRequest,db: Session = Depends(get_db)): 
    change_establishment = db.query(Establishment).filter(Establishment.id == id_establishment).first()
    if change_establishment is None:
        raise HTTPException(
            status_code=404,
            detail="establishment no encontrado"
        )
    
    for key, value in employeeChange.dict().items():
        setattr(
            change_establishment, 
            key, value
        )
    
    db.commit()
    db.refresh(change_establishment)
    return change_establishment

@establishmentRoutes.delete("/establishment/${id_employee}", response_model=EstablishmentResponse)
async def delete_establishment(id_employee: int, db: Session = Depends(get_db)):
    delete_employee = db.query(Establishment).filter(Establishment.id == id_employee).first()
    if delete_employee is None:
        raise HTTPException(
            status_code=404, 
            detail="establishment no encontrado"
        )
    
    db.delete(delete_employee)
    db.commit()
    return delete_employee
    