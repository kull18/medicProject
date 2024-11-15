from sqlalchemy.orm import Session
from app.schemas.User import UserRequest
from app.models.User import user
from app.shared.utils.security import hash_password
from fastapi import HTTPException


def createUser(db: Session, employee_data: UserRequest):
    try:
        hashed_password = hash_password(employee_data.contraseña)
        
        db_user = user(
            id_rol=employee_data.id_rol,
            nombre=employee_data.nombre,
            contraseña=hashed_password,
            id_establecimiento=employee_data.id_establecimiento,
            id_servicio=employee_data.id_servicio
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear el usuario: {str(e)}")


def getUsers(db:Session):
    datos =   db.query(user).all()
    return datos