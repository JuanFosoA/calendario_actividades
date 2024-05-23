from sqlalchemy import func, select
from models import Homework
from schemas.UserSchema import Student
from src.schemas.CourseSchema import Course as CourseSchema
from src.schemas.CourseSchema import CourseCreate as CoursecreateSchema
from src.models.Course import Course as CourseModel
from src.repositories.user import UserRepository, student_course_association


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
    
    def get_total_homework_duration(self, course_id: int) -> int:
        total_duration = self.db.query(
            func.sum(Homework.duration)
        ).filter(Homework.course_id == course_id).scalar()
        return total_duration or 0

    def get_course_students(self, course_id:int) -> list[int]:
        result = self.db.execute(
            select([student_course_association.student_id])
            .where(student_course_association.course_id == course_id)
        ).fetchall()
        return [row[0] for row in result]
    
    def get_media_charge_homework(self, course_id: int) -> int:
        student_couses = self.get_course_students(course_id)
        hours = 0
        for i in student_couses:
            hours += UserRepository(self.db).get_student_taks_charge(i)
        return hours/len(student_couses)
    