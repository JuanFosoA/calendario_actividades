from fastapi import APIRouter, Body, Depends, HTTPException, Security, status
from fastapi.responses import JSONResponse
from typing import Annotated, Union
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.encoders import jsonable_encoder
from src.repositories.auth import AuthRepository
from src.schemas.UserSchema import UserLogin as UserLoginSchema
from src.schemas.UserSchema import StudentCreate as StudentCreateSchema, TeacherCreate as TeacherCreateSchema, User, UserCreate as UserCreateSchema
from src.auth.has_access import security

auth_router = APIRouter()


@auth_router.post(
    "/register",
    tags=["auth"],
    response_model=dict,
    description="Register a new user",
)
def register_user(user: StudentCreateSchema = Body()) -> dict:
    try:
        new_user = AuthRepository().register_student(user)
        return JSONResponse(
            content={
                "message": "The user was successfully registered",
                "data": jsonable_encoder(new_user),
            },
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as err:
        return JSONResponse(
            content={"message": str(err), "data": None},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    
@auth_router.post(
    "/login", tags=["auth"], response_model=dict, description="Authenticate an user"
)
def login_user(user: UserLoginSchema) -> dict:
    try:
        access_token, refresh_token = AuthRepository().login_user(user)
        return JSONResponse(
            content={"access_token": access_token, "refresh_token": refresh_token},
            status_code=status.HTTP_200_OK,
        )
    except Exception:
        return JSONResponse(
            content={"message": "Invalid credentials", "data": None},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
