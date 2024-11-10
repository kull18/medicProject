from fastapi import APIRouter; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.config.db import engine, get_db, Base
import app.models
from app.models.type_establishment import TypeEstablishment
from app.schemas.type_establishment import Type_establishmentRequest, Type_establishmentResponse
from app.models.type_stablishmentModel import Type_establishmentResponse
Base.metadata.create_all(bind=engine)


type_establishmentRoutes = APIRouter(
    tags=["type_establishment"],
    deprecated=False
) 


@type_establishmentRoutes.post('/type_establishment/', status_code=status.HTTP_201_CREATED, response_model=Type_establishmentResponse)
async def create_rol(post_type_establishment: Type_establishmentRequest, db: Session = Depends(get_db)):
    new_type_establishment = TypeEstablishment(**post_type_establishment.model_dump())
    db.add(new_type_establishment)
    db.commit()
    db.refresh(new_type_establishment)
    return new_type_establishment.__dict__



@type_establishmentRoutes.get('/type_establishment/', status_code= status.HTTP_200_OK, response_model= List[Type_establishmentResponse])
async def get_type_establishments(db: Session = Depends(get_db)):
    all_type_establishments = db.query(TypeEstablishment).all(); 
    for i in all_type_establishments:
        print("type_establishment" + i.serviciocol)
    return all_type_establishments; 


@type_establishmentRoutes.put("/type_establishment/${id_type_establishment}", response_model=Type_establishmentResponse)
async def change_type_establishment(id_type_establishment: int, userChange: Type_establishmentRequest,db: Session = Depends(get_db)): 
    change_type_establishment = db.query(TypeEstablishment).filter(TypeEstablishment.id_tipo_establecimiento == id_type_establishment).first()
    if change_type_establishment is None:
        raise HTTPException(
            status_code=404,
            detail="type_establishment no encontrado"
        )
    
    for key, value in userChange.dict().items():
        setattr(
            change_type_establishment, 
            key, value
        )
    
    db.commit()
    db.refresh(change_type_establishment)
    return change_type_establishment

@type_establishmentRoutes.delete("/type_establishment/${id_type_establishment}", response_model=Type_establishmentResponse)
async def delete_type_establishment(id_type_establishment: int, db: Session = Depends(get_db)):
    delete_type_establishment = db.query(TypeEstablishment).filter(TypeEstablishment.id_tipo_establecimiento == id_type_establishment).first()
    if delete_type_establishment is None:
    
        raise HTTPException(
            status_code=404, 
            detail="type_establishment no encontrado"
        )
    
    db.delete(delete_type_establishment)
    db.commit()
    return delete_type_establishment
    