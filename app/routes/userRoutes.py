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
from app.models.ScheduleDoctor import ScheduleDoctor
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
        
    try:
      db_user = createUser(db=db, employee_data=post_user)
      return db_user
    except Exception as e:
       return e
        
@userRoutes.get('/user/', status_code= status.HTTP_200_OK, response_model= List[UserResponse])
async def get_employees(db: Session = Depends(get_db)):

    try:
      all_users = db.query(user).all(); 
      return all_users; 
    except Exception as e:
        return e; 

@userRoutes.get("/establishmentInformation/", status_code=status.HTTP_200_OK)
async def establishment_information(db: Session = Depends(get_db)):

    try:
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
    except Exception as e:
       return e
    
@userRoutes.get("/allInformationService/", status_code=status.HTTP_200_OK)
async def get_all_Information_Service(db: Session = Depends(get_db)):

    try:
      all_information_service = db.query(user, Establishment).join(Establishment, Establishment.id_establecimiento == user.id_establecimiento).all() 
      data_all_information_service = []; 

      for medic, establishment in all_information_service:
        data_all_information_service.append({
            "id_medic": medic.id_usuario,
            "medicName": medic.nombre,
            "id_establishment": establishment.id_establecimiento,
            "nameEstablishment": establishment.nombre
      })

      return data_all_information_service
    except Exception as e:
        return e

@userRoutes.get("/allHours/", status_code=status.HTTP_200_OK)
async def get_all_hours_doctor(db: Session = Depends(get_db)):

    try:
        all_hours = db.query(user, ScheduleDoctor).join(ScheduleDoctor, user.id_usuario == ScheduleDoctor.id_usuario).all();
        data_all_hours = []

        print(all_hours)

        for user, scheduledoctor in all_hours:
            data_all_hours.append({
                "id_doctor": user.id_usuario,
                "horarios": {
                    "día": scheduledoctor.día,
                    "entrada": scheduledoctor.entrada,
                    "salida": scheduledoctor.salida
                }
            })
            return data_all_hours
    except Exception as e:
        return e
   
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
    
    try:
      change_user = db.query(user).filter(user.id_usuario == id_user).first()
      if change_user is None:

        raise HTTPException(
            status_code=404,
            detail="user no encontrado"
        )
    
      for key, value in employeeChange.dict(exclude_unset=True).items():
        setattr(
            change_user, 
            key, value
        )
    
      db.commit()
      db.refresh(change_user)
      return change_user
    except Exception as e:
       return e

@userRoutes.delete("/user/{id_user}", response_model=UserResponse)
async def delete_user(id_user: int, db: Session = Depends(get_db)):

    try:
      delete_user = db.query(user).filter(user.id_usuario == id_user).first()
      if delete_user is None:
        raise HTTPException(
            status_code=404, 
            detail="user no encontrado"
        )
    
      db.delete(delete_user)
      db.commit()
      return delete_user
    except Exception as e:
       return e