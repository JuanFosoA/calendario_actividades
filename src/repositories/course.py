from src.schemas.CourseSchema import Course as CourseSchema
from src.schemas.CourseSchema import CourseCreate as CoursecreateSchema
from src.models.Course import Course as CourseModel
from src.repositories.user import UserRepository

class CourseRepository:
    def __init__(self, db) -> None:
        self.db = db

    def get_course(self, id: int) -> CourseSchema:
        faculty = self.db.query(CourseModel).filter(CourseModel.id == id).first()
        return faculty
    
    def get_courses_by_ids(self, ids: list[int]) -> list[CourseModel]:
        return self.db.query(CourseModel).filter(CourseModel.id.in_(ids)).all()

    def create_course(self, faculty: CoursecreateSchema) -> dict:
        new_course = CourseModel(**faculty.model_dump())
        if new_course.teacher_id <= 0:
            new_course.teacher_id = None
        elif not UserRepository(self.db).get_user(new_course.teacher_id):
            new_course.teacher_id = None
        self.db.add(new_course)
        self.db.commit()
        self.db.refresh(new_course)
        return new_course
