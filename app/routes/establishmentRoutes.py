from fastapi import APIRouter, Form, Depends, UploadFile; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
import magic
from app.shared.config.db import get_db, Base
import app.models
from app.shared.config.s3Connection import getS3_connection
from app.models.Establishment import Establishment
from app.schemas.Establishment import EstablishmentRequest, EstablishmentResponse
from app.models.EstablishmentModel import EstablishmentResponse

KB = 1024 
MB = 1024 * KB
SupportedTypes = ["image/jpeg", "image/png"]
s3 = getS3_connection(); 
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


@establishmentRoutes.get('/establishment/', status_code= status.HTTP_200_OK, response_model= List[EstablishmentResponse])
async def get_establishments(db: Session = Depends(get_db)):
    all_establishments = db.query(Establishment).all(); 
    for i in all_establishments:
        print("establishment")
    return all_establishments; 


@establishmentRoutes.post("/image/", status_code= status.HTTP_200_OK)
async def postImage_establishment(id_establishment: int = Form(...),imageEstablishment: UploadFile = Form(...), db: Session = Depends(get_db)):
    id_find_imageEmployee = db.query(Establishment).filter(Establishment.id_tipo_establecimiento == id_establishment).first(); 

    if id_find_imageEmployee is None:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST
        )

    if not imageEstablishment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    content = await imageEstablishment.read(); 
    size = len(content); 
     
    if not 0 < size <= 1 * MB:
        raise HTTPException(
           status_code = status.HTTP_400_BAD_REQUEST 
        )
    
    file_type = magic.from_buffer(buffer=content, mime=True)

    if file_type not in SupportedTypes:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    await s3.upload_file(contentents=content, key="regiber"); 


@establishmentRoutes.put("/establishment/${id_establishment}", response_model=EstablishmentResponse)
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

@establishmentRoutes.delete("/establishment/${id_employee}", response_model=EstablishmentResponse)
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
    