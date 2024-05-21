from pydantic import BaseModel, Field
from typing import Optional


class Course(BaseModel):
    id: Optional[int] = Field(default=None, title="Id of the course")
    title: str = Field(max_length=100, title="Name of the course")
    is_active: bool = Field(default=True, title="Status of the course")
    teacher_id: int = Field(ge=1, title="Teacher of the course")
