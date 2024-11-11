from fastapi import APIRouter, Form, Depends, UploadFile; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
import magic
from io import BytesIO
from app.shared.config.db import get_db, Base
import app.models
from app.shared.config.s3Connection import getS3_connection
from app.models.Establishment import Establishment
from app.models.Servicie import Service
from app.schemas.Establishment import EstablishmentRequest, EstablishmentResponse
from app.models.EstablishmentModel import EstablishmentResponse
import os


SupportedTypes = ["image/jpeg", "image/png"]
s3 = getS3_connection(); 
bucketName = os.getenv("BUCKET")
establishmentRoutes = APIRouter(
    tags=["establishments"],
    deprecated=False
); 


@establishmentRoutes.post('/establishment/', status_code=status.HTTP_201_CREATED, response_model=EstablishmentResponse)
async def create_employee(post_establishment: EstablishmentRequest, db: Session = Depends(get_db)):
    new_establishment = Establishment(**post_establishment.model_dump())
    db.add(new_establishment)
    db.commit()
    db.refresh(new_establishment)
    return new_establishment.__dict__

@establishmentRoutes.get("/searchEstablishment/{name_establishment}", status_code=status.HTTP_201_CREATED, response_model=EstablishmentResponse)
async def getEstablishmentByName(name_establishment: str, db: Session = Depends(get_db)):
    establishment_name = db.query(Establishment).filter(Establishment.nombre == name_establishment).first()

    if establishment_name is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return establishment_name

@establishmentRoutes.get("/searchEstablishmentService/{type_service}", status_code=status.HTTP_201_CREATED, response_model=EstablishmentResponse)
async def getEstablishmentByName(type_service: str, db: Session = Depends(get_db)):
    establishment_name = db.query(Service, Establishment).join(Establishment).filter(Service.tipo == type_service).all()

    if establishment_name is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return establishment_name

@establishmentRoutes.get('/establishment/', status_code= status.HTTP_200_OK, response_model= List[EstablishmentResponse])
async def get_establishments(db: Session = Depends(get_db)):
    all_establishments = db.query(Establishment).all(); 
    for i in all_establishments:
        print("establishment")
    return all_establishments; 

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
    change_establishment = db.query(Establishment).filter(Establishment.id_establecimiento == id_establishment).first()
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

@establishmentRoutes.delete("/establishment/{id_employee}", response_model=EstablishmentResponse)
async def delete_establishment(id_establishment: int, db: Session = Depends(get_db)):
    delete_establishment = db.query(Establishment).filter(Establishment.id_establecimiento == id_establishment).first()
    if delete_establishment is None:
        raise HTTPException(
            status_code=404, 
            detail="establishment no encontrado"
        )
    
    db.delete(delete_establishment)
    db.commit()
    return delete_establishment
    