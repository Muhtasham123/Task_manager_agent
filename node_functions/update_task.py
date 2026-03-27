from states.tm_state import TaskManagerState
from langchain.tools import tool

@tool
def update_task(state : TaskManagerState):
    """LLM node for deciding which task to update"""
    return {}