from fastapi import APIRouter, Form, Depends; 
from fastapi import FastAPI, Depends,status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.shared.utils.security import hash_password
from app.shared.config.db import engine, get_db, Base
import app.models
from fastapi.responses import JSONResponse
from app.services.authService import loguearse
from app.models.User import user
from app.schemas.TokenModel import AccessToken
from app.services.employeeService import createUser
from app.schemas.type_establishment import Type_establishmentResponse
from app.schemas.User import UserRequest,UserLoginReques, UserResponse
from app.models.UserModel import UserResponse

userRoutes = APIRouter(
    tags=["user"],
    deprecated=False
); 


@userRoutes.post('/user/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(post_user: UserRequest, db: Session = Depends(get_db)):
        db_user = createUser(db=db, employee_data=post_user)
        return db_user

@userRoutes.get('/user/', status_code= status.HTTP_200_OK, response_model= List[UserResponse])
async def get_employees(db: Session = Depends(get_db)):
    all_users = db.query(user).all(); 
    for i in all_users:
        print("user" + i.nombre)
    return all_users; 


@userRoutes.post("/login", response_model=AccessToken)
async def login_user(user: UserLoginReques, db: Session = Depends(get_db)):
    try:
        userFind = loguearse(Employee=user, db=db)
        
        if not userFind:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="error al logear"
            )
        
        response = JSONResponse(content={"access_token": userFind.access_token, "token_type": "bearer"})
        response.headers["Authorization"] = f"Bearer {userFind.access_token}"

        return AccessToken(access_token=userFind.access_token, data_user=userFind.data_user)
    except HTTPException as e:
        raise e 

@userRoutes.put("/user/{id_user}", response_model=UserResponse)
async def change_user(id_user: int, employeeChange: UserRequest,db: Session = Depends(get_db)): 
    change_user = db.query(user).filter(user.id_usuario == id_user).first()
    if change_user is None:

        raise HTTPException(
            status_code=404,
            detail="user no encontrado"
        )
    
    for key, value in employeeChange.dict().items():
        setattr(
            change_user, 
            key, value
        )
    
    db.commit()
    db.refresh(change_user)
    return change_user

@userRoutes.delete("/user/{id_user}", response_model=UserResponse)
async def delete_user(id_user: int, db: Session = Depends(get_db)):
    delete_user = db.query(user).filter(user.id_usuario == id_user).first()
    if delete_user is None:
        raise HTTPException(
            status_code=404, 
            detail="user no encontrado"
        )
    
    db.delete(delete_user)
    db.commit()
    return delete_user
    