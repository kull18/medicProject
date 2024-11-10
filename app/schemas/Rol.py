from pydantic import BaseModel; 


class RolBase(BaseModel):
    id_rol: int
    description: str

    class config:
        orm_mode = True

class rolRequest(RolBase):
    class config:
        orm_mode = True

class rolResponse(RolBase):
    id: int


    class config:
        orm_mode = True