from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.User import UserLoginReques
from app.models.User import user
from app.models.Rol import rol
from app.shared.utils.security import verify_password
from app.shared.middlewares.generateToken import generateToken
from app.schemas.TokenModel import AccessToken, DataUserToken
from app.models.Establishment import Establishment

def loguearse(Employee: UserLoginReques, db: Session):
    db_user = db.query(user).filter(user.nombre == Employee.nombre).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El empleado no está registrado"
        )

    if not verify_password(Employee.contraseña, db_user.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta"
        )
    
    role = db.query(rol).filter(rol.id_rol == db_user.id_rol).first()
    id_establishment = db.query(Establishment).filter(Establishment.id_establecimiento == db_user.id_establecimiento).first()

    if id_establishment is None:
        id_establishment_value = None
    else:
        id_establishment_value = id_establishment.id_establecimiento
        
    data_user = DataUserToken(
        nombre=db_user.nombre,
        id_rol=db_user.id_rol, 
        id_usuario=db_user.id_usuario,
        rol= role.description,
        id_establecimiento = id_establishment_value
    )

    access_token = generateToken(data={"nombre": db_user.nombre, "id_rol": db_user.id_rol})

    return AccessToken(access_token=access_token, data_user=data_user)