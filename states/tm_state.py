from typing import TypedDict, Literal, Annotated, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

# Defining State of the workflow
class TaskManagerState(TypedDict):
    messages:Annotated[list[BaseMessage], add_messages]
    summary:str
    task_statement:str
    task:dict
    iterations:int
    max_iterations:int