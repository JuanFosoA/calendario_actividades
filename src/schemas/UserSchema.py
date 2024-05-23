from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from src.schemas.CourseSchema import Course


class Faculty(BaseModel):
    id: int
    name: str = Field(min_length=10, max_length=60)

class FacultyCreate(BaseModel):
    name: str = Field(min_length=10, max_length=60)

class User(BaseModel):
    id: Optional[int] = Field(default=None, title="Id of the user")
    name: str = Field(min_length=4, max_length=60, title="Name of the user")
    email: EmailStr = Field(min_length=6, max_length=64, title="Email of theuser")
    password: str = Field(max_length=64, title="Password of the user")
    is_active: bool = Field(default=True, title="Status of the user")
    user_type: str = Field(..., pattern="^(admin|student|teacher)$")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "pepe@base.net",
                "name": "Pepe Pimentón",
                "password": "xxx",
                "is_active": True,
            }
        }


class Admin(User):
    pass


class Student(User):
    semester: int = Field(default=None, ge=1, le=10)


class Teacher(User):
    Faculty_id: Optional[int]
    Courses_ids: Optional[List[int]]


class UserCreate(BaseModel):
    name: str = Field(min_length=4, max_length=60, title="Name of the user")
    email: EmailStr = Field(min_length=6, max_length=64, title="Email of the user")
    password: str = Field(max_length=64, title="Password of the user")

class TeacherCreate(UserCreate):
    faculty_id: Optional[int]
    

class StudentCreate(UserCreate):
    semester: Optional[int] = Field(le=10)

class assign_student_course(BaseModel):
    student_id: int
    course_id: int


class UserLogin(BaseModel):
    email: EmailStr = Field(
        min_length=6, max_length=64, alias="username", title="Email of the user"
    )
    password: str = Field(min_length=4, title="Password of the user")
