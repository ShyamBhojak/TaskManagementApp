from fastapi import FastAPI
from src.utils.db import Base, engine
# from src.tasks.models import Task
from src.users.models import User
from src.tasks.router import task_routes
from src.users.router import user_routes

Base.metadata.create_all(engine)

app = FastAPI(
    title="Task Management App",
    description="",
    version="1.0.0"
)
app.include_router(task_routes)
app.include_router(user_routes)
