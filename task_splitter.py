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
5. If user says anything besides to perform an action, just store user query as it is
in the task list.
"""

max_retries = 2

def split_tasks(query, try_no):
    messages = [SystemMessage(system_message)]
    human_message = HumanMessage(query)
    messages.append(human_message)
    
    response = structured_model.invoke(messages).model_dump()

    if response['unsure']:
        return response['msg']

    return response['tasks']
