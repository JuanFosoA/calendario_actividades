from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.config.database import Base
from src.models.Course import Course

student_course_association = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("course_id", Integer, ForeignKey("courses.id")),
)


class Faculty(Base):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=100), unique=True, index=True)
    teachers = relationship("Teacher", back_populates="faculty")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(length=64), unique=True, index=True)
    name = Column(String(length=60))
    password = Column(String(length=64))
    is_active = Column(Boolean, default=True)
    user_type = Column(String(length=50), index=True)

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": user_type,
    }


class Admin(User):
    __tablename__ = "admins"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }


class Student(User):
    __tablename__ = "students"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    semester = Column(Integer, default=None)
    courses = relationship(
        "Course", secondary=student_course_association, back_populates="students"
    )

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }


class Teacher(User):
    __tablename__ = "teachers"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    faculty_id = Column(Integer, ForeignKey("faculties.id"))
    faculty = relationship("Faculty", back_populates="teachers")
    courses = relationship("Course", back_populates="teacher")

    __mapper_args__ = {
        "polymorphic_identity": "teacher",
    }
