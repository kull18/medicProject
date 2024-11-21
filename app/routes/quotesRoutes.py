from fastapi import APIRouter, Depends; 
from fastapi import  Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.config.db import get_db
from app.models.Quotes import quotes
from app.schemas.Quotes import QuotesRequest, QuotesResponse
from app.models.QuotesModel import QuotesResponse
from app.models.Establishment import Establishment
from app.models.User import user

quotesRoutes = APIRouter(
    tags=["quotes"],
    deprecated=False
); 


@quotesRoutes.post('/quotes/', status_code=status.HTTP_201_CREATED, response_model=QuotesResponse)
async def create_employee(post_quote: QuotesRequest, db: Session = Depends(get_db)):

    try:
      new_quote = quotes(**post_quote.model_dump())
      db.add(new_quote)
      db.commit()
      db.refresh(new_quote)
      return new_quote.__dict__
    except Exception as e:
        return e

@quotesRoutes.get('/quotes/', status_code= status.HTTP_200_OK, response_model= List[QuotesResponse])
async def get_quotes(db: Session = Depends(get_db)):

    try:
      all_quotes = db.query(quotes).all(); 
      return all_quotes; 
    except Exception as e:
        return e; 

@quotesRoutes.get("/quotesById/{patientId}/{status}", status_code=status.HTTP_200_OK)
async def getQuotesById(patientId: int,status: str,bd: Session = Depends(get_db)):
   
   try:
      quotesById = bd.query(quotes).filter(quotes.id_usuario == patientId).filter(quotes.estatus == status).all()
      return quotesById
   except Exception as e:
      return e; 


@quotesRoutes.get("/quotesById/{patientId}/{status}", status_code=status.HTTP_200_OK)
async def getQuotesById(patientId: int,status: str,bd: Session = Depends(get_db)):
   
   try:
      quotesById = bd.query(quotes).filter(quotes.id_usuario == patientId).filter(quotes.estatus == status).all()
      return quotesById
   except Exception as e:
      return e; 

@quotesRoutes.get("/quotesByIdDoctor/{id_doctor}/{status}", status_code=status.HTTP_200_OK)
async def getQuotesById(id_doctor: int,status: str,bd: Session = Depends(get_db)):
   
   try:
      quotesById = bd.query(quotes, user).join(user, user.id_usuario == quotes.id_doctor).filter(quotes.id_doctor == id_doctor).filter(quotes.estatus == status).all()
      return quotesById
   except Exception as e:
      return e; 

@quotesRoutes.get("/quotesByIdRecepcionist/{id_doctor}/{status}", status_code=status.HTTP_200_OK)
async def getQuotesById(id_doctor: int,status: str,bd: Session = Depends(get_db)):
   
   try:
      quotesById = bd.query(quotes, user).join(user, user.id_usuario == quotes.id_doctor).filter(quotes.id_doctor == id_doctor).filter(quotes.estatus == status).all()
      return quotesById
   except Exception as e:
      return e; 
@quotesRoutes.put("/quotes/{id_quote}", response_model=QuotesResponse)
async def change_quote(id_quote: int, quoteChange: QuotesRequest,db: Session = Depends(get_db)): 

    try:
      change_quote = db.query(quotes).filter(quotes.id_cita == id_quote).first()
      if change_quote is None:
        raise HTTPException(
            status_code=404,
            detail="quote no encontrado"
        )
    
      for key, value in quoteChange.dict(exclude_unset=True).items():
        setattr(
            change_quote, 
            key, value
        )
    
      db.commit()
      db.refresh(change_quote)
      return change_quote
    except Exception as e:
       return e
    
@quotesRoutes.delete("/quotes/{id_quote}", response_model=QuotesResponse)
async def delete_quote(id_quote: int, db: Session = Depends(get_db)):
    
    try:
      delete_quote = db.query(quotes).filter(quotes.id_cita == id_quote).first()
      if delete_quote is None:
        raise HTTPException(
            status_code=404, 
            detail="quote no encontrado"
        )
    
      db.delete(delete_quote)
      db.commit()
      return delete_quote
    except Exception as e:
       return e