from pydantic import BaseModel; 

class rolResponse(BaseModel):
    name: str

class config:
    orm_mode = True