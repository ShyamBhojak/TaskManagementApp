from fastapi import APIRouter, Depends
from src.tasks import controller
from src.tasks.dtos import TaskSchema
from src.utils.db import get_db


task_routes = APIRouter(prefix="/tasks")


@task_routes.post("/create")
def createtask(data:TaskSchema, db = Depends(get_db)): #(db)using dependency injection
    return controller.createtask(data, db)

@task_routes.get("/")
def get_all_tasks(db = Depends(get_db)):
    return controller.get_tasks(db)

@task_routes.get("/{task_id}")
def get_all_tasks(task_id: int, db = Depends(get_db)):
    return controller.get_tasks(task_id, db)