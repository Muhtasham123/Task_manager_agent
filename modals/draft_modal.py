from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from node_functions.create_draft import create_draft

load_dotenv()

tools = [create_draft]
                   
initial_modal = ChatOpenAI(
    model="gpt-4o-mini",
    temperature = 0.5
)

modal = initial_modal.bind_tools(tools, parallel_tool_calls=False)