from fastapi import APIRouter, Form, Depends; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.utils.security import hash_password
from app.shared.config.db import engine, get_db, Base
import app.models
from app.models.EstablishmentModel import EstablishmentResponse
from fastapi.responses import JSONResponse
from app.services.authService import loguearse
from app.models.User import user
from app.models.Establishment import Establishment
from app.schemas.TokenModel import AccessToken
from app.services.employeeService import createUser
from app.schemas.type_establishment import Type_establishmentResponse
from app.schemas.User import UserRequest,UserLoginReques, UserResponse
from app.models.UserModel import UserResponse
from app.models.type_establishment import TypeEstablishment
from app.models.Schedule import Schedule

userRoutes = APIRouter(
    tags=["user"],
    deprecated=False
); 


@userRoutes.post('/user/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(post_user: UserRequest, db: Session = Depends(get_db)):
        db_user = createUser(db=db, employee_data=post_user)
        return db_user

@userRoutes.get('/user/', status_code= status.HTTP_200_OK, response_model= List[UserResponse])
async def get_employees(db: Session = Depends(get_db)):
    all_users = db.query(user).all(); 
    for i in all_users:
        print("user" + i.nombre)
    return all_users; 


@userRoutes.get("/establishmentInformation/", status_code=status.HTTP_200_OK)
async def establishment_information(db: Session = Depends(get_db)):
    establishemnts = db.query(Establishment, Schedule, TypeEstablishment).join(Schedule, Establishment.id_horario == Schedule.id_horario).join(TypeEstablishment, Establishment.id_tipo_establecimiento == TypeEstablishment.id_tipo_establecimiento).all()
    results = []; 

    print(establishemnts)
    for establecimiento, horario, tipo_establecimiento in establishemnts:
        results.append({
            "id _establecimiento": establecimiento.id_establecimiento,
            "nombre": establecimiento.nombre,
            "descripción":establecimiento.descripción,
            "entrada": horario.entrada,
            "salida": horario.salida,
            "tipo_establecimiento": tipo_establecimiento.tipo
     })
        return results

@userRoutes.get("/allInformationService/", status_code=status.HTTP_200_OK)
async def get_all_Information_Service(db: Session = Depends(get_db)):
    all_information_service = db.query(user, Establishment).join(Establishment, user.id_establecimiento == Establishment.id_establecimiento).all(); 
    data_all_information_service = []; 

    for medic, establishment in all_information_service:
        data_all_information_service.append({
            "id_medic": medic.id_usuario,
            "medicName": medic.nombre,
            "id_establishment": establishment.id_establecimiento,
            "nameEstablishment": establishment.nombre
        })
    return data_all_information_service

@userRoutes.post("/login", response_model=AccessToken)
async def login_user(user: UserLoginReques, db: Session = Depends(get_db)):
    try:
        userFind = loguearse(Employee=user, db=db)
        
        if not userFind:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Error al logear"
         )
        
        data_user = userFind.data_user.dict() if hasattr(userFind.data_user, "dict") else userFind.data_user

        response = JSONResponse(
            content={
                "token_access": userFind.access_token, 
                "type_token": "bearer",
                "data_user": data_user
            }
        )

        response.headers["Authorization"] = f"Bearer {userFind.access_token}"

        return response
    except HTTPException as e:
        raise e

@userRoutes.put("/user/{id_user}", response_model=UserResponse)
async def change_user(id_user: int, employeeChange: UserRequest,db: Session = Depends(get_db)): 
    change_user = db.query(user).filter(user.id_usuario == id_user).first()
    if change_user is None:

        raise HTTPException(
            status_code=404,
            detail="user no encontrado"
        )
    
    for key, value in employeeChange.dict().items():
        setattr(
            change_user, 
            key, value
        )
    
    db.commit()
    db.refresh(change_user)
    return change_user

@userRoutes.delete("/user/{id_user}", response_model=UserResponse)
async def delete_user(id_user: int, db: Session = Depends(get_db)):
    delete_user = db.query(user).filter(user.id_usuario == id_user).first()
    if delete_user is None:
        raise HTTPException(
            status_code=404, 
            detail="user no encontrado"
        )
    
    db.delete(delete_user)
    db.commit()
    return delete_user
    