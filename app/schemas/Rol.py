from pydantic import BaseModel; 


class RolBase(BaseModel):
    description: str

    class Config:
        orm_mode = True

class rolRequest(RolBase):
    class Config:
        orm_mode = True

class rolResponse(RolBase):
    id: int

    class Config:
        orm_mode = True