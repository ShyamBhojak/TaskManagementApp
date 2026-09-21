from pydantic import BaseModel

class TaskSchema(BaseModel):
    title:str
    description:str
    isCompleted : bool = False

# To send particular fields in response
class TaskResponseSchema(BaseModel):
    id:int
    title:str
    description:str
    isCompleted : bool