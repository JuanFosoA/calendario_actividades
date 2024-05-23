from fastapi import APIRouter, Body, Depends, status, Query, Path
from fastapi.responses import JSONResponse
from typing import Annotated, Union
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.encoders import jsonable_encoder
from src.config.database import SessionLocal
from src.auth.has_access import security
from src.auth import auth_handler
from typing import List

from src.schemas.UserSchema import Teacher, TeacherCreate
from src.repositories.user import UserRepository
from src.repositories.auth import AuthRepository

teacher_router = APIRouter()


@teacher_router.post(
    "/",
    tags=["teachers"],
    response_model=dict,
    description="Creates a new teacher"
)
def create_teacher(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    teacher: TeacherCreate = Body(),
) -> dict:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        user_id = auth_handler.decode_token(credential)["user.id"]
        if UserRepository(db).get_user_type(user_id) == "admin":
            new_course = AuthRepository().register_teacher(teacher)
            return JSONResponse(
                content={
                    "message": "The ingreso was successfully created",
                    "data": jsonable_encoder(new_course),
                },
                status_code=status.HTTP_201_CREATED,
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


@teacher_router.get(
    "/",
    tags=["teachers"],
    response_model=List[Teacher],
    description="Returns all teachers stored",
)
def get_all_teachers(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> List[Teacher]:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        user_id = auth_handler.decode_token(credential)["user.id"]
        user = UserRepository(db).get_user(user_id)
        if user.user_type == "admin":
            result = UserRepository(db).get_users("teacher")
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


@teacher_router.get(
    "/{id}",
    tags=["teachers"],
    response_model=Teacher,
    description="Returns data of one specific teacher",
)
def get_teacher(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(ge=1, le=5000),
) -> Teacher:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        user_id = auth_handler.decode_token(credential)["user.id"]
        user = UserRepository(db).get_user(user_id)
        if user.user_type == "admin" and UserRepository(db).get_user_type(id) == "teacher":
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


@teacher_router.put(
    "/{id}",
    tags=["teachers"],
    response_model=dict,
    description="Updates the data of specific teacher",
)
def update_teacher(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(ge=1),
    student: TeacherCreate = Body(),
) -> dict:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        user_id = auth_handler.decode_token(credential)["user.id"]
        user = UserRepository(db).get_user(user_id)
        if user.user_type == "admin" and UserRepository(db).get_user_type(id) == "teacher":
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


@teacher_router.delete(
    "/{id}",
    tags=["teachers"],
    response_model=dict,
    description="Removes specific teacher",
)
def remove_teacher(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(ge=1),
) -> dict:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        user_id = auth_handler.decode_token(credential)["user.id"]
        user = UserRepository(db).get_user(user_id)
        if user.user_type == "admin" and UserRepository(db).get_user_type(id) == "teacher":
            UserRepository(db).delete_user(id)
            return JSONResponse(
                content={
                    "message": "The student was removed successfully", "data": None},
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
