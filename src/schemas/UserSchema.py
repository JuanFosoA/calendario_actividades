from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class Faculty(BaseModel):
    name: str = Field(min_length=10, max_length=60)

class User(BaseModel):
    id: Optional[int] = Field(default=None, title="Id of the user")
    name: str = Field(min_length=4, max_length=60, title="Name of the user")
    email: EmailStr = Field(min_length=6, max_length=64, title="Email of theuser")
    password: str = Field(max_length=64, title="Password of the user")
    is_active: bool = Field(default=True, title="Status of the user")

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
    permission: bool = Field(default=True)

class Student(User):
    
    semester: int = Field(default=None, min_length=1, max_length=10)
    
    
class Teacher(User):
    
    faculty: Faculty