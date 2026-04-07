from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from node_functions.create_task import create_task
from node_functions.delete_task import delete_task
from node_functions.update_task import update_task
from node_functions.access_db import access_db

load_dotenv()

tools = [create_task, delete_task, update_task, access_db]

initial_modal = ChatOpenAI(
    model="gpt-4o-mini",
    temperature = 0
)

modal = initial_modal.bind_tools(tools, parallel_tool_calls=False)