from langchain_core.messages import ToolMessage
from langchain.tools import tool, ToolRuntime
from db.queries import delete_task as delete_task_in_db
from db.vector_store import vec_store
from pydantic import BaseModel, Field

class DeleteSchema(BaseModel):
    task_id : int = Field(description="Id of task to be deleted")

@tool(args_schema = DeleteSchema)
def delete_task(task_id:int, runtime:ToolRuntime):

    """LLM node for deleteing task from database"""
    print("Using delete_task tool....")
    
    # deleting task from actual database

    delete_task_in_db(task_id)

    return ToolMessage(
        content="Success",
        tool_name="delete_task",
        tool_call_id=runtime.tool_call_id
    )