from fastapi import APIRouter, Form,Depends, UploadFile, File;
from datetime import datetime 
from fastapi import Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.config.db import  get_db
from app.models.Campaigns import campaigns
from app.shared.config.s3Connection import get_s3_connection
from app.schemas.Campaigns import CampaignsRequest, CampaignsResponse
from app.models.CampaignsModel import CampaignsResponse
from app.services.S3sevice import get_s3_connection
from app.models.Establishment import Establishment

campaignsRoutes = APIRouter(
    tags=["campaigns"],
    deprecated=False
); 


@campaignsRoutes.post('/campaigns/', status_code=status.HTTP_201_CREATED)
async def create_caipaign(
   nombre: str = Form(...),
   descripción: str = Form(...),
   dirección: str = Form(...),
   público: str = Form(...),
   fecha_inicio: datetime = Form(...),
   id_establecimiento: int = Form(...),
   db: Session = Depends(get_db),
   file: UploadFile = File(...)
):
    
    try:
      post_campaign = {
         "nombre": nombre,
         "descripción": descripción,
         "dirección": dirección,
         "público": público,
         "fecha_inicio": fecha_inicio,
         "id_establecimiento": id_establecimiento
      }

      db.begin()

      new_campaign = campaigns(**post_campaign)
      db.add(new_campaign)
      db.commit()
      db.refresh(new_campaign)

      try:
            s3 = get_s3_connection()

            if not file: 
               raise HTTPException(
                  status_code=status.HTTP_400_BAD_REQUEST,
                  detail="No se cargo ninguna imagen "
            )

            file_content = await file.read()
            print(file.filename)
            
            bucket_name = "upmedicproject4c2"
            object_name = f"campaigns/{new_campaign.id_campañas}/{file.filename}"
            s3.put_object(Bucket=bucket_name, Key=object_name, Body=file_content)
            return {
                "message": f"Archivo subido correctamente a s3://{bucket_name}/{object_name}",
                "establishment": new_campaign
            }
        
      except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al subir la imagen de la campaña: {e}"
            )
    except Exception as e:
       db.rollback()
       raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail="error al generar consulta"
       )

@campaignsRoutes.get('/campaignsAll/{location}', status_code= status.HTTP_200_OK)
async def get_employees(location: str,db: Session = Depends(get_db)):

    try:

      s3 = get_s3_connection()
      response = s3.list_objects_v2(Bucket="upmedicproject4c2")

      if 'Contents' not in response:
         raise HTTPException(status_code=404, detail="no se encontraron elementos")
      
      images = []
      for obj in response['Contents']:
         file_key = obj['Key']
         if file_key.endswith(('.jpg', '.jpeg', '.png')):  
                image_url = f"https://upmedicproject4c2.s3.amazonaws.com/{file_key}"
                images.append(image_url)

      all_campaigns = db.query(campaigns, Establishment).join(Establishment, campaigns.id_establecimiento == Establishment.id_establecimiento).filter(Establishment.localidad == location); 
      
      data_all_campaigns = []
      for campaign, establishment in all_campaigns:
         nombre_image = f"campaigns/{campaign.id_campañas}"
         print(nombre_image)
         for image in images: 
            if nombre_image in image:
               data_all_campaigns.append({
                  "campaign": campaign,
                  "image": image                  
               })
      return data_all_campaigns
    except Exception as e:
       return e; 

@campaignsRoutes.get('/campaigns/{id_establishment}', status_code= status.HTTP_200_OK)
async def get_employees(id_establishment: int,db: Session = Depends(get_db)):

    try:

      s3 = get_s3_connection()
      response = s3.list_objects_v2(Bucket="upmedicproject4c2")

      if 'Contents' not in response:
         raise HTTPException(status_code=404, detail="no se encontraron elementos")
      
      images = []
      for obj in response['Contents']:
         file_key = obj['Key']
         if file_key.endswith(('.jpg', '.jpeg', '.png')):  
                image_url = f"https://upmedicproject4c2.s3.amazonaws.com/{file_key}"
                images.append(image_url)

      all_campaigns = db.query(campaigns).filter(campaigns.id_establecimiento == id_establishment).all(); 

      data_all_campaigns = []
      for campaign in all_campaigns:
         nombre_image = f"campaigns/{campaign.id_campañas}"
         for image in images: 
            if nombre_image in image:
               data_all_campaigns.append({
                  "campaign": campaign,
                  "image": image                  
               })
      return data_all_campaigns
    except Exception as e:
       return e; 


@campaignsRoutes.get('/campaignsByName/{campaign_name}/{location}', status_code= status.HTTP_200_OK)
async def get_employees(campaign_name: str,location: str,db: Session = Depends(get_db)):

    try:

        s3 = get_s3_connection()
        response = s3.list_objects_v2(Bucket="upmedicproject4c2")
        
        if 'Contents' not in response:
            raise HTTPException(status_code=404, detail="No elements found in S3")
        
        images = []
        for obj in response['Contents']:
            file_key = obj['Key']
            if file_key.endswith(('.jpg', '.jpeg', '.png')):
                image_url = f"https://upmedicproject4c2.s3.amazonaws.com/{file_key}"
                images.append(image_url)
        
       
        all_campaigns = db.query(campaigns, Establishment).join(Establishment, Establishment.id_establecimiento == campaigns.id_establecimiento).filter(Establishment.localidad == location).filter(campaigns.nombre == campaign_name).all()
        
        data_all_campaigns = []
        for campaign, establishment in all_campaigns:
            nombre_image = f"campaigns/{campaign.id_campañas}"
            for image in images:
                if nombre_image in image:
                    data_all_campaigns.append({
                        "campaign": campaign,
                        "image": image
                    })
        
        return data_all_campaigns
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@campaignsRoutes.get('/campaignsByEstablishmentName/{id_establishment}/{name}', status_code= status.HTTP_200_OK)
async def get_employees(id_establishment: int,name: str,db: Session = Depends(get_db)):

    try:

        s3 = get_s3_connection()
        response = s3.list_objects_v2(Bucket="upmedicproject4c2")
        
        if 'Contents' not in response:
            raise HTTPException(status_code=404, detail="No elements found in S3")
        
        # Get all images
        images = []
        for obj in response['Contents']:
            file_key = obj['Key']
            if file_key.endswith(('.jpg', '.jpeg', '.png')):
                image_url = f"https://upmedicproject4c2.s3.amazonaws.com/{file_key}"
                images.append(image_url)
        
       
        all_campaigns = db.query(campaigns, Establishment).join(Establishment, Establishment.id_establecimiento == campaigns.id_establecimiento).filter(Establishment.id_establecimiento == id_establishment).filter(campaigns.nombre == name).all()
        
        # Build list of campaigns with corresponding images
        data_all_campaigns = []
        for campaign, establishment in all_campaigns:
            nombre_image = f"campaigns/{campaign.id_campañas}"
            for image in images:
                if nombre_image in image:
                    data_all_campaigns.append({
                        "campaign": campaign,
                        "image": image
                    })
        
        return data_all_campaigns
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@campaignsRoutes.get('/campaignsWithOut/', status_code= status.HTTP_200_OK)
async def get_employees(db: Session = Depends(get_db)):

    try:

      s3 = get_s3_connection()
      response = s3.list_objects_v2(Bucket="upmedicproject4c2")

      if 'Contents' not in response:
         raise HTTPException(status_code=404, detail="no se encontraron elementos")
      
      images = []
      for obj in response['Contents']:
         file_key = obj['Key']
         if file_key.endswith(('.jpg', '.jpeg', '.png')):  
                image_url = f"https://upmedicproject4c2.s3.amazonaws.com/{file_key}"
                images.append(image_url)

      all_campaigns = db.query(campaigns).all(); 

      data_all_campaigns = []
      for campaign in all_campaigns:
         nombre_image = f"campaigns/{campaign.id_campañas}"
         for image in images: 
            if nombre_image in image:
               data_all_campaigns.append({
                  "campaign": campaign,
                  "image": image                  
               })
      return data_all_campaigns
    except Exception as e:
       return e; 

@campaignsRoutes.put("/campaigns/{id_campaign}")
async def change_campaign(id_campaign: int, campaignChanges: CampaignsRequest,db: Session = Depends(get_db)): 

    try:
      change_campaign = db.query(campaigns).filter(campaigns.id_campañas == id_campaign).first()
      if change_campaign is None:

        raise HTTPException(
            status_code=404,
            detail="campaign no encontrado"
        )
    
      for key, value in campaignChanges.dict(exclude_unset=True).items():
        setattr(
            change_campaign, 
            key, value
        )
    
      db.commit()
      db.refresh(change_campaign)
      return change_campaign
    except Exception as e:
       return e 
    
@campaignsRoutes.delete("/campaignDelete/{id_campaign}", response_model=CampaignsResponse)
async def delete_campaign(id_campaign: int, db: Session = Depends(get_db)):
    
    try:
      delete_campaign = db.query(campaigns).filter(campaigns.id_campañas == id_campaign).first()
      if delete_campaign is None:
        raise HTTPException(
            status_code=404, 
            detail="campaign no encontrado"
        )
      db.delete(delete_campaign)
      db.commit()
      return delete_campaign
    except Exception as e:
       return e; 