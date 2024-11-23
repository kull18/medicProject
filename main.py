from fastapi import FastAPI
from app.shared.config.db import engine, get_db, Base
import app.models
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.routes.rolRouter import rolRoutes
from app.routes.addressRoutes import addressRoutes
from app.routes.type_establishmentRoutes import type_establishmentRoutes
from app.routes.quotesRoutes import quotesRoutes
from app.routes.billRoutes import billRoutes
from app.routes.scheduleRoutes import scheduleRoutes
from app.routes.serviceDoctorRoutes import scheduleDoctorRoutes
from app.routes.establishmentRoutes import establishmentRoutes
from app.routes.userRoutes import userRoutes
from app.routes.serviceRouter import serviceRoutes
from app.routes.campaignsRoutes import campaignsRoutes
from app.routes.StripeRoute import stripe_router
from app.routes.braitingRoute import braitingRoutes
load_dotenv(); 

app = FastAPI()

#iter routes
routes = [ rolRoutes, userRoutes, scheduleDoctorRoutes, scheduleRoutes,campaignsRoutes,addressRoutes, quotesRoutes,serviceRoutes,type_establishmentRoutes,establishmentRoutes, billRoutes, stripe_router, braitingRoutes]
for route  in routes:
    app.include_router(route)

origins = [
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

