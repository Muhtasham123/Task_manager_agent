from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

class SplitSchema(BaseModel):
    tasks:list[str] = Field(description="list of tasks")
    unsure:Literal[True, False]
    msg:str

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature = 0
)

structured_model = model.with_structured_output(SplitSchema)

system_message = f"""You are an assistant that splits user input into separate tasks. If you are confuse about anything, just set unsure true, task list empty and your message in msg, for clarification. Do not ask for additional information. You must keep meta data of each task with its statement.

Instructions:

1. Split input only if there are clearly independent actions. 

2. If there is one complex goal, do NOT split.
3. Keep tasks as full sentences.
4. Output must strictly follow the JSON format: tasks (list of strings), unsure (True/False), msg (string).
"""

messages = [SystemMessage(system_message)]
max_retries = 2

def split_tasks(res_msg, try_no):
    
    user_input = input(res_msg)
    human_message = HumanMessage(user_input)
    messages.append(human_message)
    
    response = structured_model.invoke(messages).model_dump()

    if response['unsure'] and try_no <= max_retries:
        return split_tasks(response['msg'], try_no + 1)

    return response['tasks']
