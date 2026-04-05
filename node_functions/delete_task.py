from langchain_core.messages import ToolMessage
from langchain.tools import tool, ToolRuntime
from db.queries import delete_task as delete_task_in_db
from db.queries import fetch_specific_tasks
from db.vector_store import vec_store
from pydantic import BaseModel, Field
from langgraph.types import interrupt
import json

class DeleteSchema(BaseModel):
    task_ids : list = Field(description="list of Ids of tasks to be deleted")

@tool(args_schema = DeleteSchema)
def delete_task(task_ids:list, runtime:ToolRuntime):

    """LLM node for deleteing tasks from database"""
    print("Using delete_task tool....")

    tasks_to_delete = fetch_specific_tasks(task_ids)

    decision = interrupt({
        'tasks':json.dumps(tasks_to_delete, default=str),
        'msg':'These tasks are found. Should I proceed with deletion?(yes/no)'     
    })

    if decision == 'no':
        return "Deletion canceled by user"
    
    # deleting task from actual database

    success = "Success"
    is_deleted = delete_task_in_db(task_ids)

    if not is_deleted:
        success = "Failed"
    
    return success