from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.config.database import Base

class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    due_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    course = relationship('Course', back_populates="assignments")
    
    __mapper_args__ = {
        "polymorphic_identity": "assignment",
        "polymorphic_on": "type",
    }
    

class Exam(Assignment):
    __tablename__ = "exams"
    
    duration = Column(Integer, min_length=30)
    
    __mapper_args__ = {
        "polymorphic_identity": "exam",
    }
    