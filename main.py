from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pymongo.mongo_client import MongoClient
from app.shared.config.db import engine, get_db, Base
from app.shared.config.mongoConnection import client
import app.models
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.shared.middlewares import authMiddleWare
from app.routes.rolRouter import rolRoutes
from app.routes.addressRoutes import addressRoutes
from app.routes.billRoutes import billRoutes
from app.routes.type_establishmentRoutes import type_establishmentRoutes
from app.routes.quotesRoutes import quotesRoutes
from app.routes.scheduleRoutes import scheduleRoutes
from app.routes.serviceDoctorRoutes import scheduleDoctorRoutes
from app.routes.establishmentRoutes import establishmentRoutes
from app.routes.employeeRouter import employeeRoutes
from app.routes.serviceRouter import serviceRoutes
from app.routes.campaignsRoutes import campaignsRoutes

load_dotenv(); 

app = FastAPI()


#iter routes
routes = [ rolRoutes, employeeRoutes, scheduleDoctorRoutes, scheduleRoutes,campaignsRoutes,addressRoutes, quotesRoutes,serviceRoutes,type_establishmentRoutes,establishmentRoutes, billRoutes]
for route  in routes:
    app.include_router(route)

origins = [
    "http://localhost:4200/"
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

