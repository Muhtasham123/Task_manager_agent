#---------------------- IMPORTS SECTION ---------------------------

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from task_splitter import split_tasks
from concurrent.futures import ThreadPoolExecutor
from node_functions.create_task import create_task
from node_functions.delete_task import delete_task
from node_functions.update_task import update_task
from node_functions.chat import chat
from node_functions.find_task import find_task
from langgraph.prebuilt import ToolNode, tools_condition
import os
from states.tm_state import TaskManagerState
import db.create_tables
import db.vector_store

from prompt import system_prompt
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel
from fastapi import FastAPI

#------------------------------------------------------------------

#-------------------- GRAPH CONFIGURATIO SECTION -------------------
# Creating graph instance
graph = StateGraph(TaskManagerState)

# Adding nodes into graph
tools = [create_task, delete_task, update_task, find_task]
tool_node = ToolNode(tools)

graph.add_node('chat',chat)
graph.add_node('tools',tool_node)

# Adding edges into graph
graph.add_edge(START, 'chat')
graph.add_conditional_edges('chat', tools_condition)
graph.add_edge('tools', 'chat')
graph.add_edge('chat', END)

# Compiling graph
checkpointer = InMemorySaver()
task_manager_workflow = graph.compile(checkpointer=checkpointer)


#Visualizing graph
# png_bytes = task_manager_workflow.get_graph().draw_mermaid_png()

# with open("workflow.png", "wb") as f:
#     f.write(png_bytes)

# os.startfile("workflow.png")

#-----------------------------------------------------------------------

#-------------------------- GRAPH EXECUTION FUNCTION --------------------
def execute_workflow(task, chat_id):

    config = {'configurable': {'thread_id': chat_id}}

    initial_state = {
        'messages': [HumanMessage(task)],
        'iterations': 0,
        'max_iterations': 2
    }

    return task_manager_workflow.invoke(initial_state, config)

#------------------------------------------------------------------------

#---------------------------- REQUEST ENDPOINT --------------------------

class RequestSchema(BaseModel):
    query:str
    chat_id:str

app = FastAPI()

@app.post("/chat")
async def execute_query(req: RequestSchema):
    query = req.query
    chat_id = req.chat_id

    #task_list = split_tasks(query, 1)
    #print(task_list)

    # if not task_list:
    #     return {"message": "No tasks detected"}

    # final_state = [
    #     execute_workflow(task, chat_id)
    #     for task in task_list
    # ]
    #msgs = [state['messages'][-1].content for state in final_state]

    final_state = execute_workflow(query, chat_id)
    msgs = final_state['messages'][-1].content


    return {"message": msgs}