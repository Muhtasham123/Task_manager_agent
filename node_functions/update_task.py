#-------------------------------------IMPORTS--------------------------------------------
from langchain_core.messages import ToolMessage
from langchain.tools import tool, ToolRuntime
from db.queries import update_task as update_task_in_db
from db.queries import fetch_specific_tasks
from pydantic import BaseModel, Field
from typing import Literal, List
from langgraph.types import interrupt
import json
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

    tasks_ids = [task.task_id for task in tasks_list]
    old_tasks = fetch_specific_tasks(tasks_ids)
    old_tasks_clean = []

    for old_task in old_tasks:
        old_task.pop('created_at')
        old_task['due_time'] = str(old_task['due_time'])
        old_tasks_clean.append(old_task)

    if not old_tasks:
        return "No tasks found to be updated"

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

    decision = interrupt({
        'tasks':json.dumps({
            'old_tasks':old_tasks,
            'new_tasks':updation_dict_list
        }),
        'msg':'These tasks are found. Should I proceed with updation?(yes/no)'
    })

    if decision == 'no':
        return json.dumps({
            'ai_message' : 'These tasks are found. Should I proceed with deletion?(yes/no)' +str(old_tasks) + str(updation_dict_list),
            'human_message' : 'no',
            'result' : "Updation canceled by user"
        })

    elif decision == 'yes':
        result = update_task_in_db(updation_dict_list)

        return json.dumps({
            'ai_message' : 'These tasks are found. Should I proceed with deletion?(yes/no)' +str(old_tasks) + str(updation_dict_list),
            'human_message' : 'yes',
            'result' : result
        })
    else:
        return "Invalid response"
#---------------------------------------------------------------------------------------