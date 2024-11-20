from app.shared.config.s3Connection import get_s3_connection
from fastapi import HTTPException; 

def get_images_from_s3():
    try:
        s3 = get_s3_connection()
        response = s3.list_objects_v2(Bucket="upmedicproject4c")
        
        if 'Contents' not in response:
            raise HTTPException(status_code=404, detail="No se encontraron objetos en el bucket.")
        
        images = []
        for obj in response['Contents']:
            file_key = obj['Key']
            if file_key.endswith(('.jpg', '.jpeg', '.png')):
                image_url = f"https://upmedicproject4c.s3.amazonaws.com/{file_key}"
                images.append(image_url)

        if not images:
            raise HTTPException(status_code=404, detail="No se encontraron imágenes en el bucket.")
        return images
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener imágenes del bucket: {e}"
        )