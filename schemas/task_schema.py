from pydantic import BaseModel, Field
from typing import Literal 

# Creating task schema
class TaskSchema(BaseModel):
    title:str = Field(description="title of the task")
    description:str = Field(description="description of the task")
    category:Literal['work', 'personal'] = Field(description="category of the task")
    priority:Literal['high', 'medium', 'low'] = Field(description="priority of the task")
    status:Literal['pending','in progress', 'done']
    due_time:str = Field(description="deadline of the task")

