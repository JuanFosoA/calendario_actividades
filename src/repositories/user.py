from src.schemas.UserSchema import User as UserSchema, Admin as AdminSchema
from src.schemas.UserSchema import UserCreate as UserCreateSchema
from src.models.User import Student as StudentModel, Admin as AdminModel, User as UserModel
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
    
    def get_users(
        self, user_type: str
    ) -> List[UserSchema]:
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
