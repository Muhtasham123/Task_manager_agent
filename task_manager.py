#---------------------- IMPORTS SECTION ---------------------------

from langgraph.graph import StateGraph, START, END
from node_functions.create_task import create_task
from node_functions.delete_task import delete_task
from node_functions.update_task import update_task
from node_functions.chat import chat
from node_functions.long_term_memory import memory_handler
from node_functions.access_db import access_db
from langgraph.types import Command
from langgraph.checkpoint.postgres import PostgresSaver

from langgraph.prebuilt import ToolNode, tools_condition
import os
from dotenv import load_dotenv
from states.tm_state import TaskManagerState
import db.create_tables

from prompt import system_prompt
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel
from fastapi import FastAPI
from psycopg import connect
from langgraph.store.memory import InMemoryStore
from modals.embedding_modal import embedding_function 

load_dotenv()
DB_URI = os.getenv("DB_URI")

#------------------------------------------------------------------

#-------------------- GRAPH CONFIGURATION SECTION -------------------
# Creating graph instance
graph = StateGraph(TaskManagerState)

# Adding nodes into graph
tools = [create_task, delete_task, update_task, access_db]
tool_node = ToolNode(tools)

graph.add_node('memory_handler',memory_handler)
graph.add_node('chat',chat)
graph.add_node('tools',tool_node)

# Adding edges into graph
graph.add_edge(START, 'memory_handler')
graph.add_edge('memory_handler', 'chat')
graph.add_conditional_edges('chat', tools_condition)
graph.add_edge('tools', 'chat')
graph.add_edge('chat', END)

# Compiling graph with postgresSaver checkpointer
#checkpointer = InMemorySaver()

postgres_conn = connect(DB_URI)

checkpointer = PostgresSaver(postgres_conn)
store = InMemoryStore(index={"embed":embedding_function, "dims":384})

postgres_conn.autocommit = True
checkpointer.setup()

task_manager_workflow = graph.compile(checkpointer=checkpointer, store=store)

#-----------------------------------------------------------------------

#-------------------------- GRAPH EXECUTION FUNCTION --------------------
def execute_workflow(query, chat_id, req_type):

    config = {'configurable': {'thread_id': chat_id}}
    
    state_snapshot = task_manager_workflow.get_state(config)

    existing_messages = state_snapshot.values.get("messages", []) if state_snapshot else []

    if existing_messages:
        messages = [HumanMessage(query)]
    else:
        messages = [SystemMessage(system_prompt), HumanMessage(query)]

    print("Initial messages : ", messages)
    initial_state = {
        'messages': messages,
        'summary':'',
        'iterations': 0,
        'max_iterations': 2
    }

    if req_type == 'normal':
        return task_manager_workflow.invoke(initial_state, config)
    
    elif req_type == 'resume':
        
        return task_manager_workflow.invoke(Command(resume=query), config)

#------------------------------------------------------------------------

#---------------------------- REQUEST ENDPOINT --------------------------

class RequestSchema(BaseModel):
    query:str
    chat_id:str
    request_type:str

app = FastAPI()

@app.post("/chat")
async def execute_query(req: RequestSchema):
    query = req.query
    chat_id = req.chat_id
    req_type = req.request_type

    final_state = execute_workflow(query, chat_id, req_type)

    if '__interrupt__' in final_state:
        msg = final_state['__interrupt__'][0].value['msg']
        tasks_found = final_state['__interrupt__'][0].value.get('tasks')

        return {
            "message":msg,
            "tasks_found":tasks_found
        }
    
    print("FInal state : ", final_state)
    msgs = final_state['messages'][-1].content
    return {"message": msgs}