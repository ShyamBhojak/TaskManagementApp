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
def get_all_task(task_id: int, db = Depends(get_db)):
    return controller.get_task(task_id, db)

@task_routes.put("/updatetask/{task_id}")
def update_task(task_id:int, data:TaskSchema, db = Depends(get_db)):
    return controller.update_task(task_id, data, db)

@task_routes.delete("/deletetask/{task_id}")
def delete_task(task_id:int, db = Depends(get_db)):
    return controller.delete_task(task_id,db)