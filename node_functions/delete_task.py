from langchain_core.messages import ToolMessage, AIMessage, HumanMessage
from langchain.tools import tool, ToolRuntime
from db.queries import delete_task as delete_task_in_db
from db.queries import fetch_specific_tasks
from db.vector_store import vec_store
from pydantic import BaseModel, Field
from langgraph.types import interrupt
from states.tm_state import TaskManagerState
import json

class DeleteSchema(BaseModel):
    task_ids : list = Field(description="list of Ids of tasks to be deleted")

@tool(args_schema = DeleteSchema)
def delete_task(task_ids:list):

    """LLM node for deleteing tasks from database"""
    print("Using delete_task tool....")

    tasks_to_delete = fetch_specific_tasks(task_ids)

    if not tasks_to_delete:
        return "No tasks found"

    decision = interrupt({
        'tasks':json.dumps(tasks_to_delete, default=str),
        'msg':'These tasks are found. Should I proceed with deletion?(yes/no)'     
    })

    if decision == 'no':
        return json.dumps({
            'ai_message' : 'These tasks are found. Should I proceed with deletion?(yes/no)' +str(tasks_to_delete),
            'human_message' : 'no',
            'result' : "Deletion canceled by user"
        })
    
    # deleting task from actual database

    elif decision == 'yes':
        success = "Success"
        is_deleted = delete_task_in_db(task_ids)

        if not is_deleted:
            success = "Failed"

        return json.dumps({
            'ai_message' : 'These tasks are found. Should I proceed with deletion?(yes/no)' +str(tasks_to_delete),
            'human_message' : 'yes',
            'result' : success
        })
    else:
        return "Invalid response"