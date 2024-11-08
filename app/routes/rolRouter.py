from fastapi import APIRouter; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.config.db import engine, get_db, Base
import app.models
from app.models.Rol import rol
from app.schemas.Rol import rolRequest, rolResponse
from app.models.RolModel import rolResponse
Base.metadata.create_all(bind=engine)


rolRoutes = APIRouter(
    tags=["rol"],
    deprecated= False
) 


@rolRoutes.post('/rol/', status_code=status.HTTP_201_CREATED, response_model=rolResponse)
async def create_rol(post_rol: rolRequest, db: Session = Depends(get_db)):
    new_rol = rol(**post_rol.model_dump())
    db.add(new_rol)
    db.commit()
    db.refresh(new_rol)
    return new_rol.__dict__



@rolRoutes.get('/rol/', status_code= status.HTTP_200_OK, response_model= List[rolResponse])
async def get_roles(db: Session = Depends(get_db)):
    all_roles = db.query(rol).all(); 
    for i in all_roles:
        print("rol" + i.name
              )
    return all_roles; 

@rolRoutes.put("/users/${id_rol}", response_model=rolResponse)
async def change_rol(id_rol: int, userChange: rolRequest,db: Session = Depends(get_db)): 
    change_rol = db.query(rol).filter(rol.id == id_rol).first()
    if change_rol is None:
        raise HTTPException(
            status_code=404,
            detail="rol no encontrado"
        )
    
    for key, value in userChange.dict().items():
        setattr(
            change_rol, 
            key, value
        )
    
    db.commit()
    db.refresh(change_rol)
    return change_rol

@rolRoutes.delete("/rol/${id_rol}", response_model=rolResponse)
async def delete_rol(id_rol: int, db: Session = Depends(get_db)):
    delete_rol = db.query(rol).filter(rol.id == id_rol).first()
    if delete_rol is None:
    
        raise HTTPException(
            status_code=404, 
            detail="rol no encontrado"
        )
    
    db.delete(delete_rol)
    db.commit()
    return delete_rol
    