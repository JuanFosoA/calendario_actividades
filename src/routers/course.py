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
from src.schemas.UserSchema import assign_student_course
from src.repositories.course import CourseRepository
from src.repositories.user import UserRepository

course_router = APIRouter()


@course_router.post(
    "/",
    tags=["courses"],
    response_model=dict,
    description="Creates a new ingreso"
)
def create_course(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    course: CourseCreate = Body(),
) -> dict:
    try:
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
    except Exception as err:
        return JSONResponse(
            content={"message": str(err), "data": None},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

@course_router.post(
    "/assign",
    tags=["courses"],
    response_model=List[Course],
    description="Returns all teachers stored",
)
def assign_student_to_course(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    student_course: assign_student_course = Body(),
) -> dict:
    try:
        if auth_handler.verify_jwt(credentials):
            db = SessionLocal()
            credential = credentials.credentials
            user_id = auth_handler.decode_token(credential)["user.id"]
            if UserRepository(db).get_user_type(user_id) == "admin":
                new_assign = CourseRepository(db).add_student_to_course(student_course.student_id, student_course.course_id)
                return JSONResponse(
                    content={
                        "message": "The association was successfully made",
                        "data": jsonable_encoder(new_assign),
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
    except Exception as err:
        return JSONResponse(
            content={"message": str(err), "data": None},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

@course_router.get(
    "/",
    tags=["courses"],
    response_model=List[Course],
    description="Returns all teachers stored",
)
def get_all_courses(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> List[Course]:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        user_id = auth_handler.decode_token(credential)["user.id"]
        user = UserRepository(db).get_user(user_id)
        if user.user_type == "admin":
            result = CourseRepository(db).get_courses()
            return JSONResponse(
                content=jsonable_encoder(result), status_code=status.HTTP_200_OK
            )
        elif user.user_type == "student":
            result = CourseRepository(db).get_courses_by_student_id(user_id)
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



@course_router.get(
    "/{id}",
    tags=["courses"],
    response_model=Course,
    description="Returns data of one specific teacher",
)
def get_course(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(ge=1, le=5000),
) -> Course:
    if auth_handler.verify_jwt(credentials):
        db = SessionLocal()
        credential = credentials.credentials
        user_id = auth_handler.decode_token(credential)["user.id"]
        user = UserRepository(db).get_user(user_id)
        if user.user_type == "admin":
            element = CourseRepository(db).get_course(id)
            if not element:
                return JSONResponse(
                    content={
                        "message": "The requested course was not found",
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

