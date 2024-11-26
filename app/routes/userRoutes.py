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
from app.services.S3sevice import get_s3_connection
from app.models.User import user
from app.models.Establishment import Establishment
from app.schemas.TokenModel import AccessToken
from app.models.ScheduleDoctor import ScheduleDoctor
from app.models.Address import Address
from app.models.Quotes import quotes
from app.models.Servicie import Service
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
'''''
@userRoutes.get("/establishmentInformation/", status_code=status.HTTP_200_OK)
async def establishment_information(db: Session = Depends(get_db)):

    try:
      establishment_name = db.query(Establishment, Address).join(Address, Address.id_dirección == Establishment.id_dirección).all()
     
      if establishment_name is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
      print(establishment_name)
      data_establishment = []
      for establishment, address in establishment_name:
         data_establishment.append({
            "id_establecimiento": establishment.id_establecimiento,
            "nombre": establishment.nombre,
            "direccion": address
         })


      return data_establishment
    except Exception as e:
       return e
'''''  
@userRoutes.get("/allInformationService/", status_code=status.HTTP_200_OK)
async def get_all_Information_Service(db: Session = Depends(get_db)):

    try:
      all_information_service = db.query(Service, Establishment).join(Establishment, Establishment.id_establecimiento == Service.id_establecimiento).all() 
      data_all_information_service = []; 

      for service, establishment in all_information_service:
        data_all_information_service.append({
            "id_service": service.id_servicio,
            "service": service.tipo,
            "id_establishment": establishment.id_establecimiento,
            "nameEstablishment": establishment.nombre
      })

      return data_all_information_service
    except Exception as e:
        return e

@userRoutes.get("/allSerivcesDoctor/{id_service}", status_code=status.HTTP_200_OK)
async def get_all_Information_Service(id_service: int, db: Session = Depends(get_db)):
    try:
        all_information_service = db.query(Service, user, Establishment).join(
            user, user.id_servicio == Service.id_servicio
        ).join(
            Establishment, Establishment.id_establecimiento == user.id_establecimiento
        ).filter(Service.id_servicio == id_service).all()

        data_all_information_service = []

        for service, User, establishment in all_information_service:
            data_all_information_service.append({
                "id_service": service.id_servicio,
                "service": service.tipo,
                "id_doctor": User.id_usuario,
                "name": User.nombre,
                "nombre_establishment": establishment.nombre
            })

        return data_all_information_service

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@userRoutes.get("/allServiceDoctorById_establishment/{id_establishment}", status_code=status.HTTP_200_OK)
async def get_all_Information_Service(id_establishment: int, db: Session = Depends(get_db)):
    try:
        all_information_service = db.query(Service, user, Establishment).join(
            user, user.id_servicio == Service.id_servicio
        ).join(
            Establishment, Establishment.id_establecimiento == user.id_establecimiento
        ).filter(Establishment.id_establecimiento == id_establishment).all()

        data_all_information_service = []

        for service, User, establishment in all_information_service:
            data_all_information_service.append({
                "cost": service.costo,
                "id_service": service.id_servicio,
                "service": service.tipo,
                "id_doctor": User.id_usuario,
                "name": User.nombre
            })

        return data_all_information_service

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@userRoutes.get("/allInformationServiceById/{id_establishment}", status_code=status.HTTP_200_OK)
async def get_all_Information_Service(id_establishment: int,db: Session = Depends(get_db)):

    try:
      all_information_service = db.query(Service, Establishment).join(Establishment, Establishment.id_establecimiento == Service.id_establecimiento).filter(Establishment.id_establecimiento == id_establishment).all() 
      data_all_information_service = []; 

      for service, establishment in all_information_service:
        data_all_information_service.append({
            "id_service": service.id_servicio,
            "service": service.tipo,
            "id_establishment": establishment.id_establecimiento,
            "nameEstablishment": establishment.nombre
      })

      return data_all_information_service
    except Exception as e:
        return e



@userRoutes.get("/allInformationIdEstablish/{id_establishment}", status_code=status.HTTP_200_OK)
async def get_all_Information_Service(id_establishment: int, db: Session = Depends(get_db)):
    try:
        # Conexión con S3
        s3 = get_s3_connection()
        response = s3.list_objects_v2(Bucket="upmedicproject4c2")

        if 'Contents' not in response:
            raise HTTPException(status_code=404, detail="No se encontraron elementos en S3")
        
        images = []
        for obj in response['Contents']:
            file_key = obj['Key']
            if file_key.endswith(('.jpg', '.jpeg', '.png')):  
                image_url = f"https://upmedicproject4c2.s3.amazonaws.com/{file_key}"
                images.append(image_url)

        all_information_service = db.query(Establishment, Address, Service, Schedule).join(
            Address, Address.id_dirección == Establishment.id_dirección
        ).join(
            Service, Service.id_establecimiento == Establishment.id_establecimiento
        ).join(Schedule, Schedule.id_horario == Establishment.id_horario).filter(
            Establishment.id_establecimiento == id_establishment
        ).all()

        if not all_information_service:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Establecimiento no encontrado")

        establishment_data = None
        services = []


        for establishment, address, service, schedule in all_information_service:
            for image in images:
                name_image = f"establishments/{establishment.id_establecimiento}"
                if name_image in image:
                    if not establishment_data:
                        establishment_data = {
                            "id_establishment": establishment.id_establecimiento,
                            "nameEstablishment": establishment.nombre,
                            "descripcion": establishment.descripción,
                            "direccion": {
                                "calle": address.calle,
                                "colonia": address.colonia,
                                "numero": address.numero
                            },
                            "horario": schedule,
                            "image": image
                        }
            
            services.append({
                "id_service": service.id_servicio,
                "service": service.tipo,
                "costo": service.costo
            })

        establishment_data["servicios"] = services

        return establishment_data

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@userRoutes.get("/allQuoteDoctor/{id_user}", status_code=200)
async def get_all_quotes_doctor(id_user: int, db: Session = Depends(get_db)):
   try:
      query = db.query(quotes, user).join(user, user.id_usuario == quotes.id_doctor).filter(user.id_usuario == id_user).all()

      if not query:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="error al conseguir todos las citas del doctor"
         )
      quotes_doctor = []   
      for cita, doctor in query:
         quotes_doctor.append({
            "id_cita": cita.id_cita,
            "cita": cita.id_cita,
            "fecha": cita.fecha,
            "estatus": cita.estatus
         })
         return quotes_doctor
   except Exception as e:
      return e

@userRoutes.get("/allQuoteReceptioniestEstablishment/{id_establishment}/{status}", status_code=200)
async def get_all_quotes_doctor(id_establishment: int, status: str,db: Session = Depends(get_db)):
   try:
      query = db.query(quotes, user).join(user, user.id_usuario == quotes.id_doctor).filter(user.id_establecimiento == id_establishment, quotes.estatus == status).all()

      if not query:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="error al conseguir todos las citas del doctor"
         )
      quotes_doctor = []   
      for cita, doctor in query:
         quotes_doctor.append({
            "id_cita": cita.id_cita,
            "cita": cita.id_cita,
            "fecha": cita.fecha,
            "estatus": cita.estatus
         })
         return quotes_doctor
   except Exception as e:
      return e
   
@userRoutes.get("/allQuoteDoctorEstablishment/{id_establishment}/${id_doctor}/{status}", status_code=200)
async def get_all_quotes_doctor(id_doctor: int,id_establishment: int, status: str,db: Session = Depends(get_db)):
   try:
      query = db.query(quotes, user).join(user, user.id_servicio == quotes.id_servicio).filter(user.id_establecimiento == id_establishment, quotes.estatus == status, quotes.id_doctor == id_doctor).all()

      if not query:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="error al conseguir todos las citas del doctor"
         )
      quotes_doctor = []   
      for cita, doctor in query:
         quotes_doctor.append({
            "id_cita": cita.id_cita,
            "cita": cita.id_cita,
            "fecha": cita.fecha,
            "estatus": cita.estatus
         })
         return quotes_doctor
   except Exception as e:
      return e

@userRoutes.get("/getAllDataHours/{id_user}", status_code=status.HTTP_200_OK)
async def get_all_hours_doctor(id_user: int,db: Session = Depends(get_db)):

    try:
        all_hours = db.query(user, ScheduleDoctor).join(ScheduleDoctor, user.id_usuario == ScheduleDoctor.id_usuario).filter(user.id_usuario == id_user).all()
        data_all_hours = []
        for User, scheduleDoctor in all_hours:
           data_all_hours.append({
              "id_doctor": User.id_usuario,
              "name": User.nombre,
              "dia": scheduleDoctor.día, 
              "id_schedule_doctor": scheduleDoctor.id_horario,
              "entrada": scheduleDoctor.entrada,
              "salida": scheduleDoctor.salida
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