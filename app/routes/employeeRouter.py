from fastapi import APIRouter, Form, Depends; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.utils.security import hash_password
from app.shared.config.db import engine, get_db, Base
import app.models
from app.services.authService import loguearse
from app.models.Employee import employee
from app.schemas.TokenModel import Token
from app.services.employeeService import createUser
from app.schemas.Employee import EmployeeRequest,EmployeeLoginReques, EmployeeResponse
from app.models.EmployeeModel import EmployeeResponse

employeeRoutes = APIRouter(
    tags=["employees"],
    deprecated=False
); 


@employeeRoutes.post('/employee/', status_code=status.HTTP_201_CREATED, response_model=EmployeeResponse)
async def create_employee(post_employee: EmployeeRequest, db: Session = Depends(get_db)):
        db_user = createUser(db=db, employee_data=post_employee)
        return db_user

@employeeRoutes.get('/employee/', status_code= status.HTTP_200_OK, response_model= List[EmployeeResponse])
async def get_employees(db: Session = Depends(get_db)):
    all_employees = db.query(employee).all(); 
    for i in all_employees:
        print("employee" + i.nombre)
    return all_employees; 


@employeeRoutes.post("/login", response_model=Token)
async def login_employee(user: EmployeeLoginReques,db: Session = Depends(get_db)):
    try:
        userFind = loguearse(Employee=user, db=db); 
        return Token(access_token=userFind)
    except Exception as e:
        return e; 

@employeeRoutes.put("/employee/${id_employee}", response_model=EmployeeResponse)
async def change_employee(id_employee: int, employeeChange: EmployeeRequest,db: Session = Depends(get_db)): 
    change_employee = db.query(employee).filter(employee.id_empleado == id_employee).first()
    if change_employee is None:

        raise HTTPException(
            status_code=404,
            detail="employee no encontrado"
        )
    
    for key, value in employeeChange.dict().items():
        setattr(
            change_employee, 
            key, value
        )
    
    db.commit()
    db.refresh(change_employee)
    return change_employee

@employeeRoutes.delete("/employee/${id_employee}", response_model=EmployeeResponse)
async def delete_employee(id_employee: int, db: Session = Depends(get_db)):
    delete_employee = db.query(employee).filter(employee.id_empleado == id_employee).first()
    if delete_employee is None:
        raise HTTPException(
            status_code=404, 
            detail="employee no encontrado"
        )
    
    db.delete(delete_employee)
    db.commit()
    return delete_employee
    