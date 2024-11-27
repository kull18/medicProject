from fastapi import APIRouter, Form, Depends, UploadFile, File; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.config.db import get_db
from app.models.User import user
from app.models.Address import Address
from app.models.ScheduleDoctor import ScheduleDoctor
from sqlalchemy import func
from app.shared.config.s3Connection import get_s3_connection
import boto3
from app.services.S3sevice import get_images_from_s3
from app.models.Establishment import Establishment
from app.schemas.Establishment import EstablishmentRequest, EstablishmentResponse
from app.models.EstablishmentModel import EstablishmentResponse
import os
from app.models.braiting import Braiting
from botocore.exceptions import NoCredentialsError
from app.models.Servicie import Service
from app.models.type_establishment import TypeEstablishment

SupportedTypes = ["image/jpeg", "image/png"]

establishmentRoutes = APIRouter(
    tags=["establishments"],
    deprecated=False
); 


@establishmentRoutes.post('/establishment/', status_code=status.HTTP_201_CREATED)
async def create_establishment(
    id_type_establishment: int = Form(...), 
    descripción: str = Form(...),
    categoria: str = Form(...),
    id_dirección: int = Form(...),
    id_horario: int = Form(...),
    nombre: str = Form(...),
    localidad: str = Form(...),
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    try:
        
        new_establishment = Establishment(
            id_tipo_establecimiento=id_type_establishment,
            descripción=descripción,
            categoria=categoria,
            localidad = localidad,
            id_dirección=id_dirección,
            id_horario=id_horario,
            nombre=nombre
        )

        db.add(new_establishment)
        db.commit()
        db.refresh(new_establishment)

        if not new_establishment.id_establecimiento:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear el establecimiento, ID no generado"
            )

        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se cargó ninguna imagen"
            )

        try:
            s3 = get_s3_connection()  
            file_content = await file.read() 
            print(file.filename)

            bucket_name = "upmedicproject4c2"
            object_name = f"establishments/{new_establishment.id_establecimiento}/{file.filename}"

            s3.put_object(Bucket=bucket_name, Key=object_name, Body=file_content)

            return {
                "message": f"Archivo subido correctamente a s3://{bucket_name}/{object_name}",
                "establishment": new_establishment
            }

        except Exception as e:

            db.rollback()  
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al subir el archivo: {e}"
            )

    except Exception as e:
        db.rollback()  
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el establecimiento: {e}"
        )
    

@establishmentRoutes.get("/allServices/", status_code=status.HTTP_200_OK)
async def get_all_services(db: Session = Depends(get_db)):
   try:
      all_services_establishment = db.query(Service, Establishment).join(Establishment, Establishment.id_establecimiento == Service.id_establecimiento).all()
      data_services = []   
      for service, establishment in all_services_establishment:
         data_services.append({
            "service": service,
            "establishment": establishment
      })
         return data_services
   except Exception as e:
      return e
   
@establishmentRoutes.get("/searchEstablishment/{name_establishment}/{location}", status_code=status.HTTP_201_CREATED)
async def getEstablishmentByName(name_establishment: str, location: str,db: Session = Depends(get_db)):
    
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

      establishment_name = db.query(Establishment, Address).join(Address, Address.id_dirección == Establishment.id_dirección).filter(Establishment.nombre == name_establishment).filter(Establishment.localidad == location).all()
     
      if establishment_name is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
      print(establishment_name)
      data_establishment = []
      for establishment, address in establishment_name:
         nombre_image = f"establishments/{establishment.id_establecimiento}"
         for image in images:
          if nombre_image in image:
           data_establishment.append({
            "id_establecimiento": establishment.id_establecimiento,
            "nombre": establishment.nombre,
            "direccion": address,
            "image": image
         })


      return data_establishment
    except Exception as e:
        return "error: " + str(e); 

'''''
@establishmentRoutes.get("/findEstablishmentByService/{service_type}/{location}")
async def get_establishment_by_name(service_type: str, location: str,db: Session = Depends(get_db)):
   try:

    s3 = get_s3_connection()
    response = s3.list_objects_v2(Bucket="upmedicproject4c2")


    if 'Contents' not in response:
        raise HTTPException(status_code=404, detail="No se encontraron objetos en el bucket.")


    images = [
        f"https://upmedicproject4c2.s3.amazonaws.com/{obj['Key']}"
        for obj in response['Contents']
        if obj['Key'].endswith(('.jpg', '.jpeg', '.png'))
    ]


    search_establishment = (
        db.query(Establishment, Service, Address)
        .join(Service, Service.id_establecimiento == Establishment.id_establecimiento)
        .join(Address, Address.id_dirección == Establishment.id_dirección)
        .filter(Service.tipo == service_type)
        .filter(Establishment.localidad == location)
        .all()
    )

    if not search_establishment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se encontraron resultados"
        )

    data_found_establishments = []
    for establishment, service, address in search_establishment:
        nombre_image = f"establishments/{establishment.id_establecimiento}"
        for image in images:
            if nombre_image in image:
                data_found_establishments.append({
                    "id_establecimiento": establishment.id_establecimiento,
                    "nombre": establishment.nombre,
                    "dirección": address,
                    "image": image
                })

    return data_found_establishments

   except Exception as e:
    raise HTTPException(
        status_code=500,
        detail=f"Error al procesar la solicitud: {e}"
    ) 
'''''
@establishmentRoutes.get("/findEstablishmentByTypeCategory/{service_type}/{category}/{location}")
async def get_establishment_by_type_category(
    service_type: str, 
    category: str, 
    location: str,
    db: Session = Depends(get_db)
):
    try:
        s3 = get_s3_connection()
        response = s3.list_objects_v2(Bucket="upmedicproject4c2")

        if 'Contents' not in response:
            raise HTTPException(status_code=404, detail="No se encontraron objetos en el bucket.")
        
        images = []
        for obj in response['Contents']:
            file_key = obj['Key']
            if file_key.endswith(('.jpg', '.jpeg', '.png')):  
                image_url = f"https://upmedicproject4c2.s3.amazonaws.com/{file_key}"
                images.append(image_url)

        search_establishment = (
            db.query(Establishment, TypeEstablishment, Address)
            .join(TypeEstablishment, TypeEstablishment.id_tipo_establecimiento == Establishment.id_tipo_establecimiento)
            .join(Address, Address.id_dirección == Establishment.id_dirección)
            .filter(
                TypeEstablishment.tipo == service_type, 
                Establishment.categoria == category, 
                Establishment.localidad == location
            )
            .all()
        )

        if not search_establishment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se encontraron establecimientos."
            )

        data_found_establishments = []
        for establishment, type_establishment, address in search_establishment:
            image_establishment = f"establishments/{establishment.id_establecimiento}"
            
            for image in images:
                if image_establishment in image:
                    data_found_establishments.append({
                        "id_establecimiento": establishment.id_establecimiento,
                        "nombre": establishment.nombre,
                        "dirección": address,
                        "image": image
                    })
        return data_found_establishments

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la solicitud: {str(e)}"
        )

    
@establishmentRoutes.get('/establishment/', status_code= status.HTTP_200_OK, response_model= List[EstablishmentResponse])
async def get_establishments(db: Session = Depends(get_db)):

    try:
      all_establishments = db.query(Establishment).all(); 
      for i in all_establishments:
        print("establishment")
      return all_establishments; 
    except Exception as e:
       return e
    

@establishmentRoutes.get("/allImagesEstablishment/{location}", status_code=status.HTTP_200_OK)
async def get_images_from_s3(location: str,db: Session = Depends(get_db)):
    try:
        # Conexión a S3
        s3 = get_s3_connection()
        response = s3.list_objects_v2(Bucket="upmedicproject4c2")

        if 'Contents' not in response:
            raise HTTPException(status_code=404, detail="No se encontraron objetos en el bucket.")
        
        images = []
        for obj in response['Contents']:
            file_key = obj['Key']
            if file_key.endswith(('.jpg', '.jpeg', '.png')):  
                image_url = f"https://upmedicproject4c2.s3.amazonaws.com/{file_key}"
                images.append(image_url)

        print(images)

        all_establishment = (
            db.query(Establishment, Address,
                     func.avg(Braiting.calificacion).label('promedio_calificacion'))
            .join(Address, Establishment.id_dirección == Address.id_dirección)
            .outerjoin(Braiting, Braiting.id_establecimiento == Establishment.id_establecimiento)
            .group_by(Establishment.id_establecimiento, Address.id_dirección)
            .filter(Establishment.localidad == location)
            .all()
        )

        data_establishment_image = []
        for image in images:
            for establishment, address, promedio_calificacion in all_establishment:
                nombre_image = f"establishments/{establishment.id_establecimiento}"
                if nombre_image in image:
                    data_establishment_image.append({
                        "id_establecimiento": establishment.id_establecimiento,
                        "nombre": establishment.nombre,
                        "direccion": address,
                        "image": image,
                        "promedio_calificacion": promedio_calificacion if promedio_calificacion is not None else 0
                    })

        return data_establishment_image

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener imágenes del bucket: {e}"
        )
    
@establishmentRoutes.get("/findEstablishmentByService/{service}/{location}", status_code=status.HTTP_200_OK)
async def get_images_from_s3(service: str,location: str,db: Session = Depends(get_db)):
    try:
        # Conexión a S3
        s3 = get_s3_connection()
        response = s3.list_objects_v2(Bucket="upmedicproject4c2")

        if 'Contents' not in response:
            raise HTTPException(status_code=404, detail="No se encontraron objetos en el bucket.")
        
        images = []
        for obj in response['Contents']:
            file_key = obj['Key']
            if file_key.endswith(('.jpg', '.jpeg', '.png')):  
                image_url = f"https://upmedicproject4c2.s3.amazonaws.com/{file_key}"
                images.append(image_url)

        print(images)

        all_establishment = (
            db.query(Establishment, Service,Address,
                     func.avg(Braiting.calificacion).label('promedio_calificacion'))
            .join(Address, Establishment.id_dirección == Address.id_dirección)
            .join(Service, Service.id_establecimiento == Establishment.id_establecimiento)
            .outerjoin(Braiting, Braiting.id_establecimiento == Establishment.id_establecimiento)
            .group_by(Establishment.id_establecimiento, Address.id_dirección)
            .filter(Establishment.localidad == location, Service.tipo == service)
            .all()
        )

        data_establishment_image = []
        for image in images:
            for establishment, address, promedio_calificacion in all_establishment:
                nombre_image = f"establishments/{establishment.id_establecimiento}"
                if nombre_image in image:
                    data_establishment_image.append({
                        "id_establecimiento": establishment.id_establecimiento,
                        "nombre": establishment.nombre,
                        "direccion": address,
                        "image": image,
                        "promedio_calificacion": promedio_calificacion if promedio_calificacion is not None else 0
                    })

        return data_establishment_image

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener imágenes del bucket: {e}"
        )

@establishmentRoutes.put("/establishment/{id_establishment}", response_model=EstablishmentResponse)
async def change_establishment(id_establishment: int, employeeChange: EstablishmentRequest,db: Session = Depends(get_db)): 

    try:
      change_establishment = db.query(Establishment).filter(Establishment.id_establecimiento == id_establishment).first()
      if change_establishment is None:
        raise HTTPException(
            status_code=404,
            detail="establishment no encontrado"
        )
    
      for key, value in employeeChange.dict(exclude_unset=True).items():
        setattr(
            change_establishment, 
            key, value
        )
    
      db.commit()
      db.refresh(change_establishment)
      return change_establishment
    except Exception as e:
       return e
    
@establishmentRoutes.delete("/establishment/{id_employee}", response_model=EstablishmentResponse)
async def delete_establishment(id_establishment: int, db: Session = Depends(get_db)):
    
    try:
      delete_establishment = db.query(Establishment).filter(Establishment.id_establecimiento == id_establishment).first()
      if delete_establishment is None:
        raise HTTPException(
            status_code=404, 
            detail="establishment no encontrado"
        )
    
      db.delete(delete_establishment)
      db.commit()
      return delete_establishment
    except Exception as e:
       return e