#---------------------- IMPORTS SECTION ---------------------------

from langgraph.graph import StateGraph, START, END
from node_functions.draft import draft
from node_functions.create_draft import create_draft

from langgraph.prebuilt import ToolNode, tools_condition
import os
from dotenv import load_dotenv
from utils.functions import tool_router
from states.tm_state import TaskManagerState

load_dotenv()
#------------------------------------------------------------------

#-------------------- GRAPH CONFIGURATION SECTION -------------------
# Creating graph instance
graph = StateGraph(TaskManagerState)

# Adding nodes into graph
tools = [create_draft]
tool_node = ToolNode(tools)

graph.add_node('draft', draft)
graph.add_node('tools',tool_node)

# Adding edges into graph
graph.add_edge(START, 'draft')
graph.add_conditional_edges('draft', tools_condition)
#graph.add_edge('tools', 'draft')


# Compiling graph

draft_manager_workflow = graph.compile()

#-----------------------------------------------------------------------