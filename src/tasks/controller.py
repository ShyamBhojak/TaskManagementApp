from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import Task
from fastapi import HTTPException

def createtask(data:TaskSchema,db:Session):
    record = data.model_dump()
    task = Task(
        title = record['title'],
        description = record['description'],
        isCompleted = record['is_completed']
    )
    db.add(task)
    db.commit()
    db.refresh(task) 
    return {
        "status":"task created!",
        "record":task
    }

def get_tasks(db:Session):
    tasks = db.query(Task).all()
    return{
        "status":"All Tasks",
        "data":tasks
    }

def get_task(task_id:int, db:Session):
    task = db.query(Task).get(task_id)
    if not task:
        return HTTPException(404,f"Task not found at id {task_id}")
    return{
        "status":"Task Found",
        "task":task
    }

def update_task(task_id: int, data:TaskSchema, db:Session):
    task = db.query(Task).get(task_id)
    if not task:
        return HTTPException(404,f"Task not found at id {task_id}")

    # task.title = data.title
    # task.description = data.description
    # task.isCompleted = data.isCompleted

    data = data.model_dump()
    for field, value in data.items():
        setattr(task, field, value)

    db.add(task)
    db.commit()
    db.refresh(task)

    return{
        "Status":"Task Updated",
        "Task":task
    }
