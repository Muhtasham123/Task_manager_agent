#-------------------------------------IMPORTS--------------------------------------------
from langchain_core.messages import ToolMessage
from langchain.tools import tool, ToolRuntime
from db.queries import update_task as update_task_in_db
from pydantic import BaseModel, Field
from typing import Literal, List
#----------------------------------------------------------------------------------------

#-------------------------------------SCHEMAS--------------------------------------------

class TaskSchema(BaseModel):
    task_id:int = Field(description="id of the task")
    title:str = Field(description="title of the task")
    description:str = Field(description="description of the task")
    category:Literal['work', 'personal'] = Field(description="category of the task")
    priority:Literal['high', 'medium', 'low'] = Field(description="priority of the task")
    status:Literal['pending', 'in progress', 'done']
    due_time:str = Field(description="deadline of the task")

class TasksListSchema(BaseModel):
    tasks_list:List[TaskSchema] = Field(description = "List of tasks to be updated")

#---------------------------------------------------------------------------------------

#-------------------------------------TOOL----------------------------------------------

@tool(args_schema = TasksListSchema)
def update_task( runtime : ToolRuntime, tasks_list:List[TaskSchema]):

    """LLM node for updating tasks in database"""
    print("Using update_task tool....")

    # Extracting fields to be updated
    updation_dict_list = []

    for task in tasks_list:
        updation_dict = {}
        fields = {
            "id":task.task_id,
            "title":task.title,
            "description":task.description,
            "category":task.category,
            "priority":task.priority,
            "status":task.status,
            "due_time":task.due_time,
        }
    
        for key, value in fields.items():
            if value is not None:
                updation_dict[key] = value

        updation_dict_list.append(updation_dict)

    result = update_task_in_db(updation_dict_list)

    return ToolMessage(
        content = result,
        tool_name="update_task",
        tool_call_id=runtime.tool_call_id
    )
#---------------------------------------------------------------------------------------