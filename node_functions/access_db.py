from langchain_core.messages import ToolMessage
from langchain.tools import tool, ToolRuntime
from db.queries import fetch_all_tasks
import json

@tool
def access_db(runtime:ToolRuntime):

    """Tool to access all tasks in database"""

    print("Using access_db tool...")
    all_tasks = fetch_all_tasks()

    content = all_tasks

    if not len(all_tasks):
        content = "No tasks found"
    
    return ToolMessage(
        content = json.dumps(content, default=str),
        tool_name = "access_db",
        tool_call_id = runtime.tool_call_id
    )
