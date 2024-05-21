from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.config.database import Base

student_course_association = Table('student_course', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

class Faculty(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    teachers = relationship("Teacher", back_populates="faculty")
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(length=64), unique=True, index=True)
    name = Column(String(length=60))
    password = Column(String(length=64))
    is_active = Column(Boolean, default=True)
    courses = relationship("Course", secondary=student_course_association, back_populates="students")

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": "type",
    }
    
    
class Admin(User):
    __tablename__ = "admins"
    
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    permission = Column(Boolean, default=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }


class Student(User):
    __tablename__ = "students"
    
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    semester= Column(default=None, min_length=1, max_length=10)
    student_assignments = relationship('StudentAssignment', back_populates='student')
    
    __mapper_args__ = {
        "polymorphic_identity": "student",
    }

    
class Teacher(User):
    __tablename__ = "teachers"
    
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    faculty = relationship("Faculty", back_populates="teachers")
    courses = relationship("Course", back_populates="teacher")
    
    __mapper_args__ = {
        "polymorphic_identity": "teacher",
    }