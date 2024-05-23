from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from src.config.database import Base
from src.models.Homework import Activity, Homework, Exam


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=100))
    is_active = Column(Boolean, default=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)
    teacher = relationship("Teacher", back_populates="courses")
    students = relationship(
        "Student", secondary="student_course", back_populates="courses"
    )
    homeworks = relationship("Homework", back_populates="course")
    exams = relationship("Exam", back_populates="course")
