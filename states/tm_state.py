from typing import TypedDict, Literal, Annotated, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage

# Defining State of the workflow
class TaskManagerState(TypedDict):
    messages:Annotated[list[BaseMessage], add_messages]
    user_query:str
    summary:str
    task_statement:str
    task:dict
    draft_decision:Literal['need_draft', 'not_need_draft']
    iterations:int
    max_iterations:int