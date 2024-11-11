from fastapi import APIRouter, Form, Depends; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.config.db import engine, get_db, Base
import app.models
from app.models.Bill import bills
from app.schemas.Bills import BillsRequest, BillsResponse
from app.models.BillModel import BillsResponse

billRoutes = APIRouter(
    tags=["bills"],
    deprecated=False
); 


@billRoutes.post('/bills/', status_code=status.HTTP_201_CREATED, response_model=BillsResponse)
async def create_bill(post_bill: BillsRequest, db: Session = Depends(get_db)):
    new_bill = bills(**post_bill.model_dump())
    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)
    return new_bill.__dict__

@billRoutes.get('/bills/', status_code= status.HTTP_200_OK, response_model= List[BillsResponse])
async def get_employees(db: Session = Depends(get_db)):
    all_bills = db.query(bills).all(); 
    for i in all_bills:
        print("campaign" + i.descripción)
    return all_bills; 


@billRoutes.put("/bills/{folio}", response_model=BillsResponse)
async def change_bill(folio: int, billChanges: BillsRequest,db: Session = Depends(get_db)): 
    change_bill = db.query(bills).filter(bills.folio == folio).first()
    if change_bill is None:

        raise HTTPException(
            status_code=404,
            detail="bill  no encontrado"
        )
    
    for key, value in billChanges.dict().items():
        setattr(
            change_bill, 
            key, value
        )
    
    db.commit()
    db.refresh(change_bill)
    return change_bill

@billRoutes.delete("/billDelete/{id_bill}", response_model=BillsResponse)
async def delete_bill(folio: int, db: Session = Depends(get_db)):
    delete_bill = db.query(bills).filter(bills.folio == folio).first()
    if delete_bill is None:
        raise HTTPException(
            status_code=404, 
            detail="bill no encontrado"
        )
    
    db.delete(delete_bill)
    db.commit()
    return delete_bill
    