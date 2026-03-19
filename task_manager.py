from langgraph.graph import StateGraph, START, END
from conditional_functions import intent_router, eval_router
from node_functions.create_task import create_task
from node_functions.identify_intent import identify_intent
from node_functions.evaluate_task import evaluate_task
from node_functions.optimize_task import optimize_task
from node_functions.update_task import update_task
from node_functions.delete_task import delete_task
from node_functions.dates_parser import dates_parser
from node_functions.other import other
from langgraph.checkpoint.memory import InMemorySaver
from task_splitter import split_tasks
from concurrent.futures import ThreadPoolExecutor
import os
import uuid

from states.tm_state import TaskManagerState

# Creating graph
graph = StateGraph(TaskManagerState)

# Adding nodes into graph
graph.add_node('identify_intent',identify_intent)
graph.add_node('create_task',create_task)
graph.add_node('dates_parser', dates_parser)
graph.add_node('update_task',update_task)
graph.add_node('delete_task',delete_task)
graph.add_node('other',other)
# graph.add_node('evaluate_task',evaluate_task)
# graph.add_node('optimize_task',optimize_task)

# Adding edges into graph
graph.add_edge(START, 'identify_intent')

graph.add_conditional_edges('identify_intent', intent_router,{
        "create_task": "create_task",
        "update_task": "update_task",
        "delete_task": "delete_task",
        "other": "other"
})
graph.add_edge('update_task', END)
graph.add_edge('delete_task', END)
graph.add_edge('other', END)
graph.add_edge('create_task', 'dates_parser')
# graph.add_conditional_edges('evaluate_task', eval_router, {'complete':'dates_parser', 'needs_optimization':'optimize_task'})
# graph.add_edge('optimize_task', 'evaluate_task')
graph.add_edge('dates_parser', END)

# Compiling graph
checkpointer = InMemorySaver()
task_manager_workflow = graph.compile(checkpointer=checkpointer)

# Visualizing graph
# png_bytes = task_manager_workflow.get_graph().draw_mermaid_png()

# with open("workflow.png", "wb") as f:
#     f.write(png_bytes)

# os.startfile("workflow.png")


def execute_workflow(task):
    thread_id = uuid.uuid4()
    config = {'configurable':{'thread_id':thread_id}}

    initial_state = {
        'user_input':task,
        'iterations':0,
        'max_iterations':2
    }

    final_state = task_manager_workflow.invoke(initial_state, config)
    return final_state


# splitting task
user_input = "Add a task for shopping today at 5pm and another one for attending a meeting tomorrow at 10am."

task_list = split_tasks(user_input)

# Executing workflow parallely

with ThreadPoolExecutor() as executor:
    results = list(executor.map(execute_workflow, task_list))
    print(results)