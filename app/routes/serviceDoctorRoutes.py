from fastapi import APIRouter, Form, Depends; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.Schedule import Schedule
from app.models.Servicie import Service
from app.shared.config.db import get_db, Base
import app.models
from app.models.ScheduleDoctor import ScheduleDoctor
from app.models.User import user
from app.schemas.ScheduleDoctor import ScheduleDoctorRequest, ScheduleDoctorResponse
from app.models.ScheduleDoctorModel import ScheduleDoctorResponse

scheduleDoctorRoutes = APIRouter(
    tags=["scheduleDoctor"],
    deprecated=False
); 


@scheduleDoctorRoutes.post('/scheduleDoctor/', status_code=status.HTTP_201_CREATED, response_model=ScheduleDoctorResponse)
async def create_employee(post_scheduleDoctor: ScheduleDoctorRequest, db: Session = Depends(get_db)):

    try:
      new_scheduleDoctor = ScheduleDoctor(**post_scheduleDoctor.model_dump())
      db.add(new_scheduleDoctor)
      db.commit()
      db.refresh(new_scheduleDoctor)
      return new_scheduleDoctor.__dict__
    except Exception as e:
        return e

@scheduleDoctorRoutes.get('/scheduleDoctor/', status_code= status.HTTP_200_OK, response_model= List[ScheduleDoctorResponse])
async def get_quotes(db: Session = Depends(get_db)):

    try:
      all_schedules = db.query(ScheduleDoctor).all(); 
      return all_schedules; 
    except Exception as e:
        return e

@scheduleDoctorRoutes.put("/scheduleDoctor/{id_scheduleDoctor}", response_model=ScheduleDoctorResponse)
async def change_scheduleDoctor(id_scheduleDoctor: int, scheduleChange: ScheduleDoctorRequest,db: Session = Depends(get_db)): 
    
    try:
      change_scheduleDoctor  = db.query(ScheduleDoctor).filter(ScheduleDoctor.id_horario == id_scheduleDoctor).first()
      if change_scheduleDoctor is None:
        raise HTTPException(
            status_code=404,
            detail="schedule no encontrado"
        )
    
      for key, value in scheduleChange.dict(exclude_unset=True).items():
        setattr(
            change_scheduleDoctor, 
            key, value
        )
    
      db.commit()
      db.refresh(change_scheduleDoctor)
      return change_scheduleDoctor
    except Exception as e:
       return e
    
@scheduleDoctorRoutes.delete("/scheduleDoctor/{id_schedule}", response_model=ScheduleDoctorResponse)
async def delete_schedule(id_schedule: int, db: Session = Depends(get_db)):
    
    try:
      delete_schedule = db.query(ScheduleDoctor).filter(ScheduleDoctor.id_horario == id_schedule).first()
      if delete_schedule is None:
        raise HTTPException(
            status_code=404, 
            detail="quote no encontrado"
        )
    
      db.delete(delete_schedule)
      db.commit()
      return delete_schedule
    except Exception as e:
       return e