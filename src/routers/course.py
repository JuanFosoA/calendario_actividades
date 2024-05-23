from fastapi import APIRouter, Body, Depends, status, Query, Path
from fastapi.responses import JSONResponse
from typing import Annotated, Union
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.encoders import jsonable_encoder
from src.config.database import SessionLocal
from src.auth.has_access import security
from src.auth import auth_handler
from typing import List

from src.schemas.CourseSchema import Course, CourseCreate
from src.repositories.course import CourseRepository
from src.repositories.user import UserRepository

course_router = APIRouter()


@course_router.post(
    "/",
    tags=["courses"],
    response_model=dict,
    description="Creates a new ingreso"
)
def create_ingreso(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    course: CourseCreate = Body(),
) -> dict:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        user_id = auth_handler.decode_token(credential)["user.id"]
        if UserRepository(db).get_user_type(user_id) == "admin":
            new_course = CourseRepository(db).create_course(course)
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


