from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class Homework(BaseModel):
    id: Optional[int] = Field(default=None, title="Id of the assignment")
    title: str = Field(max_length=100, nullable=False, title="Name of the assignment")
    description: str = Field(max_length=500, title="Description of the assignment")
    fecha: str | None = Field(default=None, title="Entry transaction date")
    duration: int = Field(default=None, min_length=1)
    is_active: bool = Field(default=True, title="Status of the assignment")
    course_id: int = Field(ge=1, title="Course of the assignment")


class Exam(Homework):
    duration: int = Field(default=None, min_length=1)
