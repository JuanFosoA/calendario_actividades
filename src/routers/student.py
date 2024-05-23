from fastapi import APIRouter, Body, Depends, status, Query, Path
from fastapi.responses import JSONResponse
from typing import Annotated, Union
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.encoders import jsonable_encoder
from src.config.database import SessionLocal
from src.auth.has_access import security
from src.auth import auth_handler
from typing import List

from src.schemas.UserSchema import Student, StudentCreate
from src.repositories.user import UserRepository

student_router = APIRouter()


@student_router.get(
    "/",
    tags=["students"],
    response_model=List[Student],
    description="Returns all egresos stored",
)
def get_all_students(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> List[Student]:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        user_id = auth_handler.decode_token(credential)["user.id"]
        user = UserRepository(db).get_user(user_id)
        if user.user_type == "admin":
            result = UserRepository(db).get_users("student")
            return JSONResponse(
                content=jsonable_encoder(result), status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"message": "User unauthorized"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@student_router.get(
    "/{id}",
    tags=["students"],
    response_model=Student,
    description="Returns data of one specific ingreso",
)
def get_student(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(ge=1, le=5000),
) -> Student:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        user_id = auth_handler.decode_token(credential)["user.id"]
        user = UserRepository(db).get_user(user_id)
        if (
            user.user_type == "admin"
            and UserRepository(db).get_user_type(id) == "student"
        ):
            element = UserRepository(db).get_user(id)
            if not element:
                return JSONResponse(
                    content={
                        "message": "The requested student was not found",
                        "data": None,
                    },
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            return JSONResponse(
                content=jsonable_encoder(element), status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"message": "User unauthorized"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@student_router.put(
    "/{id}",
    tags=["students"],
    response_model=dict,
    description="Updates the data of specific ingreso",
)
def update_student(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(ge=1),
    student: StudentCreate = Body(),
) -> dict:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        user_id = auth_handler.decode_token(credential)["user.id"]
        user = UserRepository(db).get_user(user_id)
        if (
            user.user_type == "admin"
            and UserRepository(db).get_user_type(id) == "student"
        ):
            element = UserRepository(db).update_user(id, student)
            return JSONResponse(
                content={
                    "message": "The student was successfully updated",
                    "data": jsonable_encoder(element),
                },
                status_code=status.HTTP_200_OK,
            )
        else:
            return JSONResponse(
                content={"message": "User unauthorized"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@student_router.delete(
    "/{id}",
    tags=["students"],
    response_model=dict,
    description="Removes specific ingreso",
)
def remove_student(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(ge=1),
) -> dict:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        user_id = auth_handler.decode_token(credential)["user.id"]
        user = UserRepository(db).get_user(user_id)
        if (
            user.user_type == "admin"
            and UserRepository(db).get_user_type(id) == "student"
        ):
            UserRepository(db).delete_user(id)
            return JSONResponse(
                content={
                    "message": "The student was removed successfully",
                    "data": None,
                },
                status_code=status.HTTP_200_OK,
            )
        else:
            return JSONResponse(
                content={"message": "User unauthorized"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
    else:
        return JSONResponse(
            content={"message": "Invalid credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
