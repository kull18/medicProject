from pydantic import BaseModel; 

class rolResponse(BaseModel):
    
    description: str

    class Config:
     orm_mode = True 

