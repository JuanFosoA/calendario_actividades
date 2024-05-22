from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from src.config.database import Base


class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    is_active = Column(Boolean, default=True)
    type = Column(String(50))
    duration = Column(Integer, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
    __mapper_args__ = {
        "polymorphic_identity": "activity",
        "polymorphic_on": type,
    }

class Homework(Activity):
    __tablename__ = "homeworks"

    id = Column(Integer, ForeignKey("activities.id"), primary_key=True)
    due_date = Column(Date)

    course = relationship("Course", back_populates="homeworks")
    

    


class Exam(Activity):
    __tablename__ = "exams"

    id = Column(Integer, ForeignKey("homeworks.id"), primary_key=True)
    course = relationship("Course", back_populates="exams")
    duration = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "exam",
    }
