from src.schemas.CourseSchema import Course as CourseSchema
from src.schemas.CourseSchema import CourseCreate as CoursecreateSchema
from src.models.Course import Course as CourseModel
from src.repositories.user import UserRepository
from src.models.User import Student as StudentModel
from typing import List


class CourseRepository:
    def __init__(self, db) -> None:
        self.db = db

    def get_course(self, id: int) -> CourseSchema:
        faculty = self.db.query(CourseModel).filter(
            CourseModel.id == id).first()
        return faculty

    def get_courses(self) -> List[CoursecreateSchema]:
        query = self.db.query(CourseModel)
        return query.all()

    def get_courses_by_student_id(self, student_id: int):
        student = self.db.query(StudentModel).filter(
            StudentModel.id == student_id).first()
        if student:
            return student.courses
        else:
            return []

    def add_student_to_course(self, student_id, course_id):
        student = self.db.query(StudentModel).filter(StudentModel.id == student_id).first()
        course = self.db.query(StudentModel).filter(StudentModel.id == course_id).first()

        if student and course:
            student.add_course(course)
            self.db.commit()
            return True
        return False

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
