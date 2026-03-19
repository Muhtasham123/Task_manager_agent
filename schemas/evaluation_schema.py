from pydantic import BaseModel, Field
from typing import Literal 

# Creating evaluation schema
class EvaluationSchema(BaseModel):
    status:Literal['optimized', 'needs_optimization'] = Field(description="status of the task")
    missing_info:list[Literal['title', 'description', 'category', 'priority', 'due_time',]] = Field(default_factory=list, description="missing fields in task")
    feedback:str = Field(description="feedback of task")