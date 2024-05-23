from fastapi import HTTPException, status
from src.repositories.user import UserRepository
from src.repositories.faculty import FacultyRepository
from src.repositories.course import CourseRepository
from src.config.database import SessionLocal
from src.auth import auth_handler
from src.schemas.UserSchema import UserLogin as UserLoginSchema
from src.schemas.UserSchema import (
    StudentCreate as StudentCreateSchema,
    TeacherCreate as TeacherCreateSchema,
)
from src.schemas.UserSchema import User, UserCreate as UserCreateSchema
from src.models.User import User, Admin, Student, Teacher


class AuthRepository:
    def __init__(self) -> None:
        pass

    def register_admin(self, user: UserCreateSchema) -> dict:
        db = SessionLocal()
        if UserRepository(db).get_user_by_email(email=user.email) is not None:
            raise Exception("Account already exists")
        hashed_password = auth_handler.hash_password(password=user.password)
        new_user: UserCreateSchema = UserCreateSchema(
            name=user.name,
            email=user.email,
            password=hashed_password,
            is_active=True,
            user_type="admin",
        )
        return UserRepository(db).create_user(new_user, Admin)

    def register_student(self, user: StudentCreateSchema) -> dict:
        db = SessionLocal()
        if UserRepository(db).get_user_by_email(email=user.email) is not None:
            raise Exception("Account already exists")

        hashed_password = auth_handler.hash_password(password=user.password)
        new_user: StudentCreateSchema = StudentCreateSchema(
            name=user.name,
            email=user.email,
            password=hashed_password,
            semester=user.semester,
            is_active=True,
        )
        return UserRepository(db).create_user(new_user, Student)

    def register_teacher(self, user: TeacherCreateSchema) -> dict:
        db = SessionLocal()

        if UserRepository(db).get_user_by_email(email=user.email) is not None:
            raise Exception("Account already exists")

        if user.faculty_id <= 0:
            user.faculty_id = None
        elif not FacultyRepository(db).get_faculty(db, faculty_id=user.faculty_id):
            raise Exception("Faculty does not exist")

        hashed_password = auth_handler.hash_password(password=user.password)
        new_user: TeacherCreateSchema = TeacherCreateSchema(
            name=user.name,
            email=user.email,
            password=hashed_password,
            faculty_id=user.faculty_id,
            is_active=True,
        )
        return UserRepository(db).create_user(new_user, Teacher)

    def login_user(self, user: UserLoginSchema) -> dict:
        db = SessionLocal()
        check_user = UserRepository(db).get_user_by_email(email=user.email)
        if check_user is None:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials (1)",
            )
        if not check_user.is_active:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The user is not allowed to log in",
            )
        if not auth_handler.verify_password(user.password, check_user.password):
            print("aqui fallo 3")
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials (2)",
            )
        access_token = auth_handler.encode_token(check_user)
        refresh_token = auth_handler.encode_refresh_token(check_user)

        return access_token, refresh_token

    def get_user_by_token(self, token: str) -> User:
        try:
            payload = auth_handler.decode_token(token)
            user_email = payload["sub"]
            user = UserRepository.get_xuser(user_email)
            if not user:
                raise HTTPException(status_code=401, detail="User not found")
            return user
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=401, detail="Invalid token or user not found"
            )
