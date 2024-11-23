from pydantic import BaseModel
from typing import Optional

class DataUserToken(BaseModel):
    
    nombre: str
    id_rol: Optional[int] = None  
    id_usuario: int 
    rol: Optional[str] = None
    id_establecimiento: Optional[int] = None

class AccessToken(BaseModel):
    access_token: str
    data_user: DataUserToken