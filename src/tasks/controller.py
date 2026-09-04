from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import Task

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