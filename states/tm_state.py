from typing import TypedDict, Literal, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

# Defining State of the workflow
class TaskManagerState(TypedDict):
    messages:Annotated[list[BaseMessage], add_messages]
    task_statement:str
    task:dict