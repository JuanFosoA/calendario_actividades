from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=100))
    is_active = Column(Boolean, default=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="courses")
    students = relationship(
        "Student", secondary="student_course", back_populates="courses"
    )
    homeworks = relationship("Homework", back_populates="course")

class Homework(Base):
    __tablename__ = "homeworks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    due_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    course = relationship("Course", back_populates="homeworks")
    type = Column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "assignment",
        "polymorphic_on": type,
    }


class Exam(Homework):
    __tablename__ = "exams"

    id = Column(Integer, ForeignKey("assignments.id"), primary_key=True)
    course = relationship("Course", back_populates="exams")
    duration = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "exam",
    }
