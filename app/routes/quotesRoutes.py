from fastapi import APIRouter, Form, Depends; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.config.db import get_db, Base
import app.models
from app.models.Quotes import quotes
from app.schemas.Quotes import QuotesRequest, QuotesResponse
from app.models.QuotesModel import QuotesResponse

quotesRoutes = APIRouter(
    tags=["quotes"],
    deprecated=False
); 


@quotesRoutes.post('/quotes/', status_code=status.HTTP_201_CREATED, response_model=QuotesResponse)
async def create_employee(post_quote: QuotesRequest, db: Session = Depends(get_db)):
    new_quote = quotes(**post_quote.model_dump())
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)
    return new_quote.__dict__


@quotesRoutes.get('/quotes/', status_code= status.HTTP_200_OK, response_model= List[QuotesResponse])
async def get_quotes(db: Session = Depends(get_db)):
    all_quotes = db.query(quotes).all(); 
    return all_quotes; 


@quotesRoutes.put("/quotes/{id_quote}", response_model=QuotesResponse)
async def change_quote(id_quote: int, quoteChange: QuotesRequest,db: Session = Depends(get_db)): 
    change_quote = db.query(quotes).filter(quotes.id_cita == id_quote).first()
    if change_quote is None:
        raise HTTPException(
            status_code=404,
            detail="quote no encontrado"
        )
    
    for key, value in quoteChange.dict().items():
        setattr(
            change_quote, 
            key, value
        )
    
    db.commit()
    db.refresh(change_quote)
    return change_quote

@quotesRoutes.delete("/quotes/{id_quote}", response_model=QuotesResponse)
async def delete_quote(id_quote: int, db: Session = Depends(get_db)):
    delete_quote = db.query(quotes).filter(quotes.id_cita == id_quote).first()
    if delete_quote is None:
        raise HTTPException(
            status_code=404, 
            detail="quote no encontrado"
        )
    
    db.delete(delete_quote)
    db.commit()
    return delete_quote