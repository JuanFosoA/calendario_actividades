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
        course = self.db.query(CourseModel).filter(
            CourseModel.id == id).first()
        return course
    
    def get_course_by_student_id(self, id: int, student_id: int) -> CourseSchema:
        student = self.db.query(StudentModel).filter(StudentModel.id == student_id).first()
        if student:
            return self.get_course(id)

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
        student: StudentModel = self.db.query(StudentModel).filter(StudentModel.id == student_id).first()
        course = self.db.query(CourseModel).filter(CourseModel.id == course_id).first()

        if student and course:
            student.add_course(course)
            self.db.commit()
            return True
        return False
    
    def get_courses_by_ids(self, ids: list[int]) -> list[CourseModel]:
        return self.db.query(CourseModel).filter(CourseModel.id.in_(ids)).all()

    def update_course(self, id: int, course: CoursecreateSchema) -> dict:
        element = self.db.query(CourseModel).filter(CourseModel.id == id).first()
        element.title = course.title
        self.db.commit()
        self.db.refresh(element)
        return element
    
    def delete_user(self, id: int) -> dict:
        element: CourseModel = self.db.query(CourseModel).filter(CourseModel.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element
    
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
