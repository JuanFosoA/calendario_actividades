from fastapi import APIRouter, Body, Depends, Security, status
from fastapi.responses import JSONResponse
from typing import Annotated, Union
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.encoders import jsonable_encoder
from src.repositories.auth import AuthRepository
from src.schemas.UserSchema import UserLogin as UserLoginSchema
from src.schemas.UserSchema import StudentCreate as StudentCreateSchema, TeacherCreate as TeacherCreateSchema, User
from src.auth.has_access import security

auth_router = APIRouter()

def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> User:
    token = credentials.credentials
    user = AuthRepository().get_user_by_token(token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return user


@auth_router.post(
    "/register",
    tags=["auth"],
    response_model=dict,
    description="Register a new user",
)
def register_student(user: Union[StudentCreateSchema, TeacherCreateSchema] = Body(...),
                     current_user: User = Depends()) -> dict:
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
