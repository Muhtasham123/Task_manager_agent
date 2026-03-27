#---------------------- IMPORTS SECTION ---------------------------

from langgraph.graph import StateGraph, START, END
from conditional_functions import intent_router, eval_router
from langgraph.checkpoint.memory import InMemorySaver
from task_splitter import split_tasks
from concurrent.futures import ThreadPoolExecutor
from node_functions.create_task import create_task
from node_functions.delete_task import delete_task
from node_functions.update_task import update_task
from node_functions.chat import chat
from langgraph.prebuilt import ToolNode, tools_condition
import os
import uuid
from states.tm_state import TaskManagerState
import db.connection
import db.create_tables

#------------------------------------------------------------------


#-------------------- GRAPH CONFIGURATIO SECTION -------------------
# Creating graph instance
graph = StateGraph(TaskManagerState)

# Adding nodes into graph
tools = [create_task, delete_task, update_task]
tool_node = ToolNode(tools)

graph.add_node('chat',chat)
graph.add_node('tools',tool_node)

# Adding edges into graph
graph.add_edge(START, 'chat')
graph.add_conditional_edges('chat', tools_condition)
graph.add_edge('tools',END)
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

#-------------------------- GRAPH EXECUTION SECTION --------------------
def execute_workflow(task):
    thread_id = uuid.uuid4()
    config = {'configurable':{'thread_id':thread_id}}

    initial_state = {
        'messages':task,
        'task_statement':task,
    }

    final_state = task_manager_workflow.invoke(initial_state, config)
    return final_state


# splitting task

task_list = split_tasks("Enter your query : ", 1)

# Executing workflow parallely

with ThreadPoolExecutor() as executor:
    results = list(executor.map(execute_workflow, task_list))
    print(results)

#------------------------------------------------------------------------