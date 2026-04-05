from schemas.task_schema import TaskSchema
from langchain_core.messages import ToolMessage
from utils.functions import due_time_parser
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from db.queries import insert_task

@tool(args_schema = TaskSchema)
def create_task(
    title:str, 
    description:str, 
    category:str, 
    priority:str, 
    status:str,
    due_time:str, 
    runtime : ToolRuntime) -> Command:

    """Store task in database"""

    print("Using create_task tool....")

    parsed_date = due_time_parser(due_time)

    task = {
        "title":title,
        "description":description,
        "category":category,
        "priority":priority,
        'status':status,
        "due_time":parsed_date
    }

    task_id = insert_task(task)
    print("create_task tool")
    
    return ToolMessage(
        content=task,
        tool_name="create_task",
        tool_call_id=runtime.tool_call_id
    )
    