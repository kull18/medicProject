from fastapi import APIRouter; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.config.db import engine, get_db, Base
import app.models
from app.models.Servicie import Service
from app.schemas.Service import ServiceRequest, ServiceResponse
from app.models.ServicieModel import ServiceResponse
Base.metadata.create_all(bind=engine)


serviceRoutes = APIRouter(
    tags=["services"],
    deprecated=False
) 


@serviceRoutes.post('/service/', status_code=status.HTTP_201_CREATED, response_model=ServiceResponse)
async def create_rol(post_service: ServiceRequest, db: Session = Depends(get_db)):
    new_service = Service(**post_service.model_dump())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service.__dict__



@serviceRoutes.get('/service/', status_code= status.HTTP_200_OK, response_model= List[ServiceResponse])
async def get_services(db: Session = Depends(get_db)):
    all_services = db.query(Service).all(); 
    for i in all_services:
        print("sevice" + i.serviciocol)
    return all_services; 

@serviceRoutes.put("/services/{id_service}", response_model=ServiceResponse)
async def change_service(id_service: int, userChange: ServiceRequest,db: Session = Depends(get_db)): 
    change_service = db.query(Service).filter(Service.id_servicio == id_service).first()
    if change_service is None:
        raise HTTPException(
            status_code=404,
            detail="rol no encontrado"
        )
    
    for key, value in userChange.dict().items():
        setattr(
            change_service, 
            key, value
        )
    
    db.commit()
    db.refresh(change_service)
    return change_service

@serviceRoutes.delete("/service/{id_service}", response_model=ServiceResponse)
async def delete_service(id_service: int, db: Session = Depends(get_db)):
    delete_service = db.query(Service).filter(Service.id_servicio == id_service).first()
    if delete_service is None:
    
        raise HTTPException(
            status_code=404, 
            detail="rol no encontrado"
        )
    
    db.delete(delete_service)
    db.commit()
    return delete_service
    