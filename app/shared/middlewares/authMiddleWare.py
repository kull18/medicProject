from jose import JWTError, jwt
from fastapi import Request, HTTPException, status, Depends
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SecretKey")
ALGORITHM = "HS256"

# Dependencia para verificar el token sin pasar request explícitamente
def get_current_user(request: Request) -> str:
    token = request.headers.get("Authorization")  # se obtiene el token desde el header
    print(token)
    
    if not token or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid or missing token"
        )

    token = token.split(" ")[1]  # Extraer el token despues de "Bearer"
    
    try:
        # Decodificar el token y extraer el payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("correo") #extraemos el payload de correo
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token missing 'correo'"
            )
        return username  # Devolver el correo del token
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token"
        )