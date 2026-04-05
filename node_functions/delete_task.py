from langchain_core.messages import ToolMessage
from langchain.tools import tool, ToolRuntime
from db.queries import delete_task as delete_task_in_db
from db.vector_store import vec_store
from pydantic import BaseModel, Field

class DeleteSchema(BaseModel):
    task_ids : list = Field(description="list of Ids of tasks to be deleted")

@tool(args_schema = DeleteSchema)
def delete_task(task_ids:list, runtime:ToolRuntime):

    """LLM node for deleteing tasks from database"""
    print("Using delete_task tool....")
    
    # deleting task from actual database

    success = "Success"
    is_deleted = delete_task_in_db(task_ids)

    if not is_deleted:
        success = "Failed"

    return ToolMessage(
        content=success,
        tool_name="delete_task",
        tool_call_id=runtime.tool_call_id
    )