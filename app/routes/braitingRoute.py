from fastapi import APIRouter, Form, Depends; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.config.db import engine, get_db, Base
from app.models.Address import Address
from app.shared.middlewares.authMiddleWare import get_current_user
from app.models.braiting import Braiting
from app.schemas.Braiting import BraitingRequest, BraitingResponse
from app.models.braitingModel import BraitingModel

braitingRoutes = APIRouter(
    tags=["braiting"],
    deprecated=False
); 


@braitingRoutes.post('/braiting/', status_code=status.HTTP_201_CREATED, response_model=BraitingResponse)
async def create_braiting(braiting: BraitingRequest, db: Session = Depends(get_db)):


    if braiting.calificacion < 1 or braiting.calificacion > 5:
        raise HTTPException(status_code=400, detail="La calificación debe estar entre 1 y 5")

    db_braiting = Braiting(**braiting.model_dump())
    
    db.add(db_braiting)
    db.commit()
    db.refresh(db_braiting)
    
    return BraitingResponse.from_orm(db_braiting)
    
@braitingRoutes.put("/braitingChange/{id_address}", response_model=BraitingResponse)
async def change_address(id_address: int, employeeChange: BraitingRequest,db: Session = Depends(get_db)): 

    try:
       change_address = db.query(Address).filter(Address.id_dirección == id_address).first()
       if change_address is None:
        raise HTTPException(
            status_code=404,
            detail="address no encontrado"
        )
       for key, value in employeeChange.dict(exclude_unset=True).items():
        setattr(
            change_address, 
            key, value
        )
       db.commit()
       db.refresh(change_address)
       return change_address
    except Exception as e:
       return e; 

@braitingRoutes.delete("/braitingDelete/{id_address}", response_model=BraitingResponse)
async def delete_address(id_address: int, db: Session = Depends(get_db)):
    try: 
       delete_address = db.query(Address).filter(Address.id_dirección == id_address).first()
       if delete_address is None:
        raise HTTPException(
            status_code=404, 
            detail="address no encontrado"
        )
    
       db.delete(delete_address)
       db.commit()
       return delete_address
    except Exception as e:
       return e; 