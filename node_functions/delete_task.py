from states.tm_state import TaskManagerState
from langchain.tools import tool

@tool
def delete_task(state : TaskManagerState):
    """LLM node for deciding which task to delete"""
    return {}