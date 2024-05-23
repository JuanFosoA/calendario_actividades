from pydantic import BaseModel, Field
from typing import Optional


class ActivityBase(BaseModel):
    title: str = Field(max_length=100, nullable=False, title="Title of the activity")
    description: Optional[str] = Field(
        max_length=500, title="Description of the activity"
    )
    is_active: bool = Field(default=True, title="Status of the activity")
    type: str = Field(max_length=50, title="Type of the activity")
    duration: int = Field(default=None, ge=1, title="Duration of the activity")
    course_id: int = Field(ge=1, title="Course ID of the activity")


class Homework(ActivityBase):
    id: Optional[int] = Field(default=None, title="ID of the homework")
    due_date: Optional[str] = Field(default=None, title="Due date of the homework")
class CreateHomeworkSchema(BaseModel):
    title: str = Field(max_length=100, title="Title of the homework", nullable=False)
    description: Optional[str] = Field(max_length=500, title="Description of the homework")
    due_date: Optional[str] = Field(default=None, title="Due date of the homework")
    duration: int = Field(ge=1, title="Duration of the homework")
    is_active: bool = Field(default=True, title="Status of the homework")
    course_id: int = Field(ge=1, title="Course ID of the homework")


class CreateExamSchema(BaseModel):
    title: str = Field(max_length=100, title="Title of the exam", nullable=False)
    description: Optional[str] = Field(max_length=500, title="Description of the exam")
    duration: int = Field(ge=1, title="Duration of the exam")
    is_active: bool = Field(default=True, title="Status of the exam")
    course_id: int = Field(ge=1, title="Course ID of the exam")

    class Config:
        schema_extra = {
            "example": {
                "title": "Final Exam",
                "description": "Final exam for the course",
                "duration": 120,
                "is_active": True,
                "course_id": 1,
            }
        }

class Exam(ActivityBase):
    id: Optional[int] = Field(default=None, title="ID of the exam")

    class Config:
        schema_extra = {
            "example": {
                "title": "Final Exam",
                "description": "Final exam for the course",
                "is_active": True,
                "type": "exam",
                "duration": 120,
                "course_id": 1,
            }
        }
