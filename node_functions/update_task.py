from langchain_core.messages import ToolMessage
from utils.functions import make_updated_doc
from langchain.tools import tool, ToolRuntime
from db.queries import update_task as update_task_in_db
from db.vector_store import vec_store
from pydantic import BaseModel, Field
from typing import Literal


class TaskSchema(BaseModel):
    task_id:str = Field(description="id of the task")
    title:str = Field(description="title of the task")
    description:str = Field(description="description of the task")
    category:Literal['work', 'personal'] = Field(description="category of the task")
    priority:Literal['high', 'medium', 'low'] = Field(description="priority of the task")
    due_time:str = Field(description="deadline of the task")

@tool(args_schema = TaskSchema)
def update_task(
    task_id:str,
    title:str, 
    description:str, 
    category:str, 
    priority:str, 
    due_time:str, 
    runtime : ToolRuntime
    ):

    """LLM node for updating task in database"""
    print("Using update_task tool....")

    # Extracting fields to be updated
    updation_dict = {}

    fields = {
        "title":title,
        "description":description,
        "category":category,
        "priority":priority,
        "due_time":due_time,
    }
    
    for key, value in fields.items():
        if value:
            updation_dict[key] = value
    

    # getting task doc from vector store to update there as well

    initial_tasks_docs = vec_store.get(
        include=["documents", "metadatas"]
    )

    task_docs = [
        {
            "task_id":id_,
            "metadata":metadata
        }
        for id_, metadata in zip(initial_tasks_docs["ids"], initial_tasks_docs["metadatas"])
        if id_ == task_id
    ]

    if not task_docs:
        return ToolMessage(
        content="Task not found",
        tool_name="update_task",
        tool_call_id=runtime.tool_call_id
    )

    # getting updating doc and replacing old doc with updated one
    updated_doc = make_updated_doc(updation_dict, task_docs[0]['metadata'])
    vec_store.delete(ids=[task_docs[0]['task_id']])
    vec_store.add_documents([updated_doc], ids=[task_docs[0]['task_id']])

    update_task_in_db(task_id, updation_dict)

    return ToolMessage(
        content="Success",
        tool_name="update_task",
        tool_call_id=runtime.tool_call_id
    )