from langchain_core.messages import ToolMessage
from langchain.tools import tool, ToolRuntime
from db.vector_store import vec_store
from pydantic import BaseModel, Field
import json

class FindSchema(BaseModel):
    user_query:str = Field(description="Task related part of user query")


@tool(args_schema=FindSchema)
def find_task(user_query:str, runtime:ToolRuntime):
    """LLM node for finding the task that user is talking about"""

    print("Using find_task tool....")

    tasks = vec_store._collection.query(
        query_texts=[user_query],
        n_results=5,
        include=["documents", "metadatas", "distances"]
    )

    print(vec_store.get(include=["documents"]))

    THRESHOLD = 1.9

    similar_tasks = [
        {
            "task_id":task_id,
            "metadata":metadata,
            "similarity_score" : score
        }
        for task_id, score, metadata  in zip(tasks['ids'][0], tasks['distances'][0], tasks['metadatas'][0]) if score <= THRESHOLD
        ]

    result = {}

    if len(similar_tasks) == 0:
        result = {
            "status": "no_match",
            "tasks": []
        }

    elif len(similar_tasks) == 1:
        result = {
            "status": "success",
            "task": similar_tasks[0]
        }

    else:
        result = {
            "status": "multiple",
            "tasks": similar_tasks
        }

    print("result : ", result)
    return ToolMessage(
        content=json.dumps(result),
        tool_name="find_task",
        tool_call_id=runtime.tool_call_id
    )