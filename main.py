from fastapi import FastAPI
from src.middlewares.error_handler import ErrorHandler
from src.config.database import Base, engine
from src.routers.auth import auth_router

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
app.include_router(prefix="", router=auth_router)
Base.metadata.create_all(bind=engine)


@app.get("/api/v1")
def great():
    return {"Hello": "World"}
