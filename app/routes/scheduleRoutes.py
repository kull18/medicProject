from fastapi import APIRouter, Form, Depends; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.config.db import get_db, Base
import app.models
from app.models.Schedule import Schedule
from app.schemas.Schedule import ScheduleRequest, ScheduleResponse
from app.models.ScheduleModel import ScheduleResponse

scheduleRoutes = APIRouter(
    tags=["schedule"],
    deprecated=False
); 


@scheduleRoutes.post('/schedule/', status_code=status.HTTP_201_CREATED, response_model=ScheduleResponse)
async def create_employee(post_schedule: ScheduleRequest, db: Session = Depends(get_db)):
    new_schedule = Schedule(**post_schedule.model_dump())
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule.__dict__


@scheduleRoutes.get('/schedule/', status_code= status.HTTP_200_OK, response_model= List[ScheduleResponse])
async def get_quotes(db: Session = Depends(get_db)):
    all_schedules = db.query(Schedule).all(); 
    return all_schedules; 


@scheduleRoutes.put("/schedule/{id_schedule}", response_model=ScheduleResponse)
async def change_schedule(id_scedule: int, scheduleChange: ScheduleRequest,db: Session = Depends(get_db)): 
    change_schedule  = db.query(Schedule).filter(Schedule.id_horario == id_scedule).first()
    if change_schedule is None:
        raise HTTPException(
            status_code=404,
            detail="schedule no encontrado"
        )
    
    for key, value in scheduleChange.dict().items():
        setattr(
            change_schedule, 
            key, value
        )
    
    db.commit()
    db.refresh(change_schedule)
    return change_schedule

@scheduleRoutes.delete("/schedule/{id_schedule}", response_model=ScheduleResponse)
async def delete_schedule(id_schedule: int, db: Session = Depends(get_db)):
    delete_schedule = db.query(Schedule).filter(Schedule.id_horario == id_schedule).first()
    if delete_schedule is None:
        raise HTTPException(
            status_code=404, 
            detail="quote no encontrado"
        )
    
    db.delete(delete_schedule)
    db.commit()
    return delete_schedule