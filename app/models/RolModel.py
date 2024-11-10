from pydantic import BaseModel; 

class rolResponse(BaseModel):
    description: str

class config:
    orm_mode = True