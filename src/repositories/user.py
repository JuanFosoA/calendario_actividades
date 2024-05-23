from sqlalchemy import select
from repositories.course import CourseRepository
from src.schemas.UserSchema import User as UserSchema, Admin as AdminSchema
from src.schemas.UserSchema import UserCreate as UserCreateSchema
from src.models.User import (
    Student as StudentModel,
    student_course_association,
    Admin as AdminModel,
    User as UserModel,
)
from typing import List


class UserRepository:
    def __init__(self, db) -> None:
        self.db = db

    def get_user_by_email(self, email: str) -> UserSchema:
        user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return user

    def get_user(self, id: int) -> UserSchema:
        user = self.db.query(UserModel).filter(UserModel.id == id).first()
        return user

    def get_user_type(self, id: int) -> str:
        user = self.get_user(id)
        return user.user_type

    def get_users(self, user_type: str) -> List[UserSchema]:
        query = self.db.query(UserModel).filter(UserModel.user_type == user_type)
        return query.all()

    def update_user(self, id: int, user: UserCreateSchema) -> dict:
        element = self.db.query(UserModel).filter(UserModel.id == id).first()
        element.name = user.name
        element.email = user.email
        self.db.commit()
        self.db.refresh(element)
        return element

    def delete_user(self, id: int) -> dict:
        element: UserModel = self.db.query(UserModel).filter(UserModel.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element

    def create_user(self, user: UserCreateSchema, userModel: UserModel) -> dict:
        new_user = userModel(**user.model_dump())
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def get_student_course_ids(self, student_id: int) -> List[int]:
        result = self.db.execute(
            select([student_course_association.c.course_id])
            .where(student_course_association.c.student_id == student_id)
        ).fetchall()
        return [row[0] for row in result]
    
    def get_student_taks_charge(self, student_id: int) -> int:
        student_couses = self.get_student_course_ids(student_id)
        hours = 0
        for i in student_couses:
            hours += CourseRepository(self.db).get_total_homework_duration(i)
        return hours