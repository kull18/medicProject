from sqlalchemy import Column, Integer, String, INT
from app.shared.config.db import Base

class rol(Base):
    __tablename__ = "rol"
    
    id_rol = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=True); 

