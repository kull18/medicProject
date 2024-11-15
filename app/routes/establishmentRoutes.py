from fastapi import APIRouter, Form, Depends, UploadFile; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.config.db import get_db
from app.models.Address import Address
from app.shared.config.s3Connection import getS3_connection
from app.models.Establishment import Establishment
from app.schemas.Establishment import EstablishmentRequest, EstablishmentResponse
from app.models.EstablishmentModel import EstablishmentResponse
import os

from app.models.Servicie import Service

SupportedTypes = ["image/jpeg", "image/png"]
s3 = getS3_connection(); 
bucketName = os.getenv("BUCKET")

establishmentRoutes = APIRouter(
    tags=["establishments"],
    deprecated=False
); 


@establishmentRoutes.post('/establishment/', status_code=status.HTTP_201_CREATED, response_model=EstablishmentResponse)
async def create_employee(post_establishment: EstablishmentRequest, db: Session = Depends(get_db)):

    try:
      new_establishment = Establishment(**post_establishment.model_dump())
      db.add(new_establishment)
      db.commit()
      db.refresh(new_establishment)
      return new_establishment.__dict__
    except Exception as e:
        return e; 

@establishmentRoutes.get("/allServices/", status_code=status.HTTP_200_OK)
async def get_all_services(db: Session = Depends(get_db)):
   try:
      all_services_establishment = db.query(Service, Establishment).join(Establishment, Establishment.id_establecimiento == Service.id_establecimiento).all()
      data_services = []   
      for service, establishment in all_services_establishment:
         data_services.append({
            "service": service,
            "establishment": establishment
      })
         return data_services
   except Exception as e:
      return e
   
@establishmentRoutes.get("/searchEstablishment/{name_establishment}", status_code=status.HTTP_201_CREATED)
async def getEstablishmentByName(name_establishment: str, db: Session = Depends(get_db)):
    
    try:
      establishment_name = db.query(Establishment, Address).join(Address, Address.id_dirección == Establishment.id_dirección).filter(Establishment.nombre == name_establishment).all()
     
      if establishment_name is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
      print(establishment_name)
      data_establishment = []
      for establishment, address in establishment_name:
         data_establishment.append({
            "id_establishment": establishment.id_establecimiento,
            "name": establishment.nombre,
            "address": address
         })


      return data_establishment
    except Exception as e:
        return e; 

@establishmentRoutes.get("/findEstablishmentByService/{service_type}")
async def get_establishment_by_name(service_type: str, db: Session = Depends(get_db)):

    try:
      search_establishment = db.query(Establishment, Service, Address).join(Service, Service.id_establecimiento == Establishment.id_establecimiento).join(Address, Address.id_dirección == Establishment.id_dirección).filter(Service.tipo == service_type).all()
      if search_establishment is None: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="error al hacer la busqueda"
        )
      
      data_found_establishments = []
      for establishment, service, address in search_establishment:
        data_found_establishments.append({
            "id_establishment": establishment.id_establecimiento,
            "name": establishment.nombre,
            "address": address
       })
      return data_found_establishments
    except Exception as e:
       return e; 
   
@establishmentRoutes.get("/findEstablishmentByTypeCategory/{service_type}/{category}")
async def get_establishment_by_type_category(service_type: str, category: str,db: Session = Depends(get_db)):

    try:
      search_establishment = db.query(Establishment, Service, Address).join(Service, Service.id_establecimiento == Establishment.id_establecimiento).join(Address, Address.id_dirección == Establishment.id_dirección).filter(Service.tipo == service_type).filter(Establishment.categoria == category).all()

      if search_establishment is None: 

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="error al hacer la busqueda"
        )
    
      data_found_establishments = []
      for establishment, service, address in search_establishment:
        data_found_establishments.append({
                "id_establishment": establishment.id_establecimiento,
                "name": establishment.nombre,
                "dirección":  address
       })
      return data_found_establishments
    except Exception as e:
       return e
    
@establishmentRoutes.get('/establishment/', status_code= status.HTTP_200_OK, response_model= List[EstablishmentResponse])
async def get_establishments(db: Session = Depends(get_db)):

    try:
      all_establishments = db.query(Establishment).all(); 
      for i in all_establishments:
        print("establishment")
      return all_establishments; 
    except Exception as e:
       return e

''' 
@establishmentRoutes.post("/image/", status_code= status.HTTP_200_OK)
async def postImage_establishment(id_establishment: int,imageEstablishment: UploadFile, db: Session = Depends(get_db)):
    if not imageEstablishment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="error"
        )
    
    content = await imageEstablishment.read()
    
    file_type = magic.from_buffer(buffer=content, mime=True)

    if file_type not in SupportedTypes:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    file_like_object = BytesIO(content)


    await s3.upload_fileobj(file_like_object, bucketName, "regiber"); 

'''
@establishmentRoutes.put("/establishment/{id_establishment}", response_model=EstablishmentResponse)
async def change_establishment(id_establishment: int, employeeChange: EstablishmentRequest,db: Session = Depends(get_db)): 

    try:
      change_establishment = db.query(Establishment).filter(Establishment.id_establecimiento == id_establishment).first()
      if change_establishment is None:
        raise HTTPException(
            status_code=404,
            detail="establishment no encontrado"
        )
    
      for key, value in employeeChange.dict(exclude_unset=True).items():
        setattr(
            change_establishment, 
            key, value
        )
    
      db.commit()
      db.refresh(change_establishment)
      return change_establishment
    except Exception as e:
       return e
    
@establishmentRoutes.delete("/establishment/{id_employee}", response_model=EstablishmentResponse)
async def delete_establishment(id_establishment: int, db: Session = Depends(get_db)):
    
    try:
      delete_establishment = db.query(Establishment).filter(Establishment.id_establecimiento == id_establishment).first()
      if delete_establishment is None:
        raise HTTPException(
            status_code=404, 
            detail="establishment no encontrado"
        )
    
      db.delete(delete_establishment)
      db.commit()
      return delete_establishment
    except Exception as e:
       return e