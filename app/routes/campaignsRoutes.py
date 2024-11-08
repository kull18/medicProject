from fastapi import APIRouter, Form, Depends; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.config.db import engine, get_db, Base
import app.models
from app.models.Campaigns import campaigns
from app.schemas.Campaigns import CampaignsRequest, CampaignsResponse
from app.models.CampaignsModel import CampaignsResponse

campaignsRoutes = APIRouter(
    tags=["campaigns"],
    deprecated=False
); 


@campaignsRoutes.post('/campaigns/', status_code=status.HTTP_201_CREATED, response_model=CampaignsResponse)
async def create_caipaign(post_campaign: CampaignsRequest, db: Session = Depends(get_db)):
    new_campaign = campaigns(**post_campaign.model_dump())
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return new_campaign.__dict__

@campaignsRoutes.get('/campaigns/', status_code= status.HTTP_200_OK, response_model= List[CampaignsResponse])
async def get_employees(db: Session = Depends(get_db)):
    all_campaigns = db.query(campaigns).all(); 
    for i in all_campaigns:
        print("campaign" + i.descripción)
    return all_campaigns; 


@campaignsRoutes.put("/campaigns/${id_campaign}", response_model=CampaignsResponse)
async def change_campaign(id_campaign: int, campaignChanges: CampaignsRequest,db: Session = Depends(get_db)): 
    change_campaign = db.query(campaigns).filter(campaigns.id_campañas == id_campaign).first()
    if change_campaign is None:

        raise HTTPException(
            status_code=404,
            detail="campaign no encontrado"
        )
    
    for key, value in campaignChanges.dict().items():
        setattr(
            change_campaign, 
            key, value
        )
    
    db.commit()
    db.refresh(change_campaign)
    return change_campaign

@campaignsRoutes.delete("/campaignDelete/${id_campaign}", response_model=CampaignsResponse)
async def delete_campaign(id_campaign: int, db: Session = Depends(get_db)):
    delete_campaign = db.query(campaigns).filter(campaigns.id_campañas == id_campaign).first()
    if delete_campaign is None:
        raise HTTPException(
            status_code=404, 
            detail="campaign no encontrado"
        )
    
    db.delete(delete_campaign)
    db.commit()
    return delete_campaign
    