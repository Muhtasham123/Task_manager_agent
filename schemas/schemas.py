from pydantic import BaseModel, Field
from typing import Literal 

# Creating task schema
class TaskSchema(BaseModel):
    title:str = Field(description="title of the task")
    description:str = Field(description="description of the task")
    category:Literal['work', 'home', 'personal', 'reminder'] = Field(description="category of the task")
    priority:Literal['high', 'medium', 'low'] = Field(description="priority of the task")
    status:Literal['pending','in progress', 'done']
    due_time:str = Field(description="deadline of the task")

# Creating draft decider schema
class DraftDeciderSchema(BaseModel):
    need_draft:Literal['need_draft', 'not_need_draft']


# Creating draft generator schema
class DraftSchema(BaseModel):
    title:str = Field(description="Title of the draft")
    text:str = Field(description="Actual text of the draft")

