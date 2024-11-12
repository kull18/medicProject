from pydantic import BaseModel

class TokenData(BaseModel):
    nombre: str | None = None
    id_rol: str | None = None
