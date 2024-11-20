from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    name: str
    product: str
    price: float
    quantity: int

class QuotesRequest(BaseModel):
    items: List[Item]

class QuotesBase(BaseModel):
    id_usuario: int
    fecha: str
    horario: str
    estatus: str
    id_doctor: int
    id_servicio: int