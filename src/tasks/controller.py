from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import Task
from fastapi import HTTPException

def createtask(data:TaskSchema,db:Session):
    record = data.model_dump()
    task = Task(
        title = record['title'],
        description = record['description'],
        isCompleted = record['isCompleted']
    )
    db.add(task)
    db.commit()
    db.refresh(task) 
    # return {
    #     "status":"task created!",
    #     "record":task
    # }
    return task

def get_tasks(db:Session):
    tasks = db.query(Task).all()
    # return{
    #     "status":"All Tasks",
    #     "data":tasks
    # }
    return tasks

def get_task(task_id:int, db:Session):
    task = db.query(Task).get(task_id)
    if not task:
        return HTTPException(404,f"Task not found at id {task_id}")
    # return{
    #     "status":"Task Found",
    #     "task":task
    # }
    return task

def update_task(task_id: int, data:TaskSchema, db:Session):
    task = db.query(Task).get(task_id)
    if not task:
        return HTTPException(404,f"Task not found at id {task_id}")

    # task.title = data.title
    # task.description = data.description
    # task.isCompleted = data.isCompleted

    # short form if we have too many fields
    data = data.model_dump()
    for field, value in data.items():
        setattr(task, field, value)

    db.add(task)
    db.commit()
    db.refresh(task)

    # return{
    #     "status":"Task Updated",
    #     "task":task
    # }
    return task


def delete_task(task_id:int, db:Session):
    task = db.query(Task).get(task_id)
    if not task:
        return HTTPException(404,f"Task not found at id {task_id}")

    db.delete(task)
    db.commit()

    # return{
    #     "status":"Task Deleted",
    #     "deleted task":task
    # }
    return None
    