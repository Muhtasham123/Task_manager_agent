from typing import TypedDict, Literal

# Defining State of the workflow
class TaskManagerState(TypedDict):
    user_input:str
    intent:Literal['create_task', 'update_task', 'delete_task', 'other']
    task:dict
    missing_info:str
    feedback:str
    iterations:int
    max_iterations:int
    task_status:Literal['optimized', 'needs_optimization']