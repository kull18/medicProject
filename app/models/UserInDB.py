from pydantic import BaseModel
from app.models.User import employee

class UserInDB(employee):
    hashed_password: str
    