from src.schemas.UserSchema import User as UserSchema
from src.schemas.UserSchema import StudentCreate as StudentCreateSchema
from src.models.User import Student as StudentModel


class UserRepository:
    def __init__(self, db) -> None:
        self.db = db

    def get_user(self, email: str) -> UserSchema:
        user = self.db.query(StudentModel).filter(StudentModel.email == email).first()
        return user

    def create_user(self, user: StudentCreateSchema) -> dict:
        new_user = StudentModel(**user.model_dump())
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
