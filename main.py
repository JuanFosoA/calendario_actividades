from fastapi import FastAPI
from src.middlewares.error_handler import ErrorHandler
from src.config.database import Base, engine
from src.routers.auth import auth_router
from src.routers.student import student_router
from src.routers.teacher import teacher_router
from src.routers.course import course_router

app = FastAPI()

app.title = "Control gastos API"
app.summary = "Control gastos REST API with FastAPI and Python"
app.description = "This is a demostration of API REST using Python"
app.version = "0.1.0"

app.openapi_tags = [
    {
        "name": "web",
        "description": "Endpoints of example",
    },
    {
        "name": "auth",
        "description": "User's authentication",
    },
]

app.add_middleware(ErrorHandler)
app.include_router(prefix="/api/v1/student", router=student_router)
app.include_router(prefix="/api/v1/teacher", router=teacher_router)
app.include_router(prefix="/api/v1/course", router=course_router)
app.include_router(prefix="", router=auth_router)
Base.metadata.create_all(bind=engine)


@app.get("/api/v1")
def great():
    return {"Hello": "World"}
