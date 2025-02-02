from fastapi import APIRouter, Form, Depends; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.config.db import engine, get_db, Base
from app.models.Address import Address
from app.shared.middlewares.authMiddleWare import get_current_user
from app.schemas.Address import AddressRequest, AddressResponse
from app.models.AddressModel import AddressResponse

addressRoutes = APIRouter(
    tags=["address"],
    deprecated=False
); 

@addressRoutes.post('/address/', status_code=status.HTTP_201_CREATED, response_model=AddressResponse)
async def create_employee(post_address: AddressRequest, db: Session = Depends(get_db)):

   try:
       new_address = Address(**post_address.model_dump())
       db.add(new_address)
       db.commit()
       db.refresh(new_address)
       return new_address.__dict__
   except Exception as e:
       return e; 

@addressRoutes.get('/address/',status_code= status.HTTP_200_OK,  response_model= List[AddressResponse])
async def get_employees(db: Session = Depends(get_db)):

    try:  
       all_address = db.query(Address).all(); 
       return all_address; 
    except Exception as e:
       return e; 

@addressRoutes.put("/address/{id_address}", response_model=AddressResponse)
async def change_address(id_address: int, employeeChange: AddressRequest,db: Session = Depends(get_db)): 

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

@addressRoutes.delete("/addressDelete/{id_address}", response_model=AddressResponse)
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