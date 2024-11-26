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
from sqlalchemy.orm import aliased
from sqlalchemy import and_
from app.models.Establishment import Establishment
from app.models.Servicie import Service

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

@quotesRoutes.get("/quotesDoctorById/{patientId}", status_code=status.HTTP_200_OK)
async def getQuotesById(patientId: int,bd: Session = Depends(get_db)):
   
   try:
      quotesById = bd.query(quotes).filter(quotes.id_doctor == patientId).all()
      return quotesById
   except Exception as e:
      return e; 

@quotesRoutes.get("/allQuotePatient/{patientId}", status_code=status.HTTP_200_OK)
async def getQuotesById(patientId: int,bd: Session = Depends(get_db)):
   
   try:
      quotesById = bd.query(quotes).filter(quotes.id_usuario == patientId).all()
      return quotesById
   except Exception as e:
      return e; 

@quotesRoutes.get("/quotesByIdRecepcionist/{id_establecimiento}", status_code=status.HTTP_200_OK)
async def getQuotesByEstablishment(id_establecimiento: int, bd: Session = Depends(get_db)):
    try:
        doctor = aliased(user)
        servicio = aliased(Service)
        establecimiento = aliased(Establishment)

        quotesByEstablishment = bd.query(quotes, servicio, establecimiento).\
            join(servicio, servicio.id_servicio == quotes.id_servicio).\
            join(establecimiento, establecimiento.id_establecimiento == servicio.id_establecimiento).\
            filter(establecimiento.id_establecimiento == id_establecimiento).\
            all()

        return quotesByEstablishment
    except Exception as e:
        return {"error": str(e)}
    


@quotesRoutes.get("/quotesByIdPatientWith/{id_patient}/{status}", status_code=status.HTTP_200_OK)
async def getQuotesById(id_patient: int, status: str, bd: Session = Depends(get_db)):
    try:
        quotesById = (
            bd.query(quotes, Service, Establishment)  
            .join(Service, Service.id_servicio == quotes.id_servicio) 
            .join(Establishment, Establishment.id_establecimiento == Service.id_establecimiento) 
            .filter(quotes.id_usuario == id_patient)  
            .filter(quotes.estatus == status) 
            .all()
        )
        result = [
            {
                'id_cita': quote.id_cita,
                'fecha': quote.fecha,
                'estatus': quote.estatus,
                'horario': quote.horario,
                'id_establecimiento': establecimiento.id_establecimiento  
            }
            for quote, servicio, establecimiento in quotesById
        ]

        return result

    except Exception as e:
        return {"error": str(e)}

@quotesRoutes.get("/quotesByIdRecepcionist/{id_establecimiento}/{status}", status_code=status.HTTP_200_OK)
async def getQuotesByEstablishment(id_establecimiento: int, status: str, bd: Session = Depends(get_db)):
    try:
        doctor = aliased(user)
        servicio = aliased(Service)
        establecimiento = aliased(Establishment)

        quotesByEstablishment = bd.query(quotes, servicio, establecimiento).\
            join(servicio, servicio.id_servicio == quotes.id_servicio).\
            join(establecimiento, establecimiento.id_establecimiento == servicio.id_establecimiento).\
            filter(establecimiento.id_establecimiento == id_establecimiento).\
            filter(quotes.estatus == status).\
            all()

        return quotesByEstablishment
    except Exception as e:
        return {"error": str(e)}
    
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