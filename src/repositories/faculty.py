from src.schemas.UserSchema import Faculty as FacultySchema
from src.schemas.UserSchema import FacultyCreate as FacultyCreateSchema
from src.models.User import Faculty as FacultyModel


class FacultyRepository:
    def __init__(self, db) -> None:
        self.db = db

    def get_faculty(self, id: int) -> FacultySchema:
        faculty = self.db.query(FacultyModel).filter(FacultyModel.id == id).first()
        return faculty

    def create_faculty(self, faculty: FacultyCreateSchema) -> dict:
        new_faculty = FacultyModel(**faculty.model_dump())
        self.db.add(new_faculty)
        self.db.commit()
        self.db.refresh(new_faculty)
        return new_faculty
