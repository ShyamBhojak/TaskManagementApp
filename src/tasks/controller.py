from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import Task
from fastapi import HTTPException
from src.users.models import User

def createtask(data:TaskSchema,db:Session,user:User):
    record = data.model_dump()
    task = Task(
        title = record['title'],
        description = record['description'],
        isCompleted = record['isCompleted'],
        user_id = user.id
    )
    db.add(task)
    db.commit()
    db.refresh(task) 
    # return {
    #     "status":"task created!",
    #     "record":task
    # }
    return task

def get_tasks(db:Session, user:User):
    tasks = db.query(Task).filter(Task.user_id == user.id).all()
    # return{
    #     "status":"All Tasks",
    #     "data":tasks
    # }
    return tasks

def get_task(task_id:int, db:Session, user:User):
    if not user or not getattr(user, "id", None):
        raise HTTPException(status_code=401, detail="Authentication required")

    task = db.query(Task).get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail=f"Task not found at id {task_id}")

    if task.user_id != user.id:
        raise HTTPException(status_code=401, detail="Unauthorized to access this task")

    # return{
    #     "status":"Task Found",
    #     "task":task
    # }
    return task

def update_task(task_id: int, data:TaskSchema, db:Session, user:User):
    task = db.query(Task).get(task_id)
    if not task:
        return HTTPException(404,f"Task not found at id {task_id}")

    if task.user_id != user.id:
        raise HTTPException(401, detail="Not allowed to update task")

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


def delete_task(task_id:int, db:Session, user:User):
    task = db.query(Task).get(task_id)
    if not task:
        return HTTPException(404,f"Task not found at id {task_id}")
    if task.user_id != user.id:
        raise HTTPException(401, "Unauthorized to delete this task")

    db.delete(task)
    db.commit()

    # return{
    #     "status":"Task Deleted",
    #     "deleted task":task
    # }
    return None
    