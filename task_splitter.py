from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Literal

class SplitSchema(BaseModel):
    tasks:list[str] = Field(description="list of tasks")
    unsure:Literal[True, False]
    msg:str

model = ChatOllama(model="phi3:mini")
structured_model = model.with_structured_output(SplitSchema)

system_message = f"""You are an assistant that splits user input into separate tasks.You must keep full information of each task and store properties like due time, priority etc for each task correctly. If you are even a little bit confuse about it, just set unsure true, task list empty and your message in msg, for clarification.

Instructions:

1. Split input only if there are clearly independent actions. 

2. If there is one complex goal, do NOT split.
3. Keep tasks as full sentences.
4. Output must strictly follow the JSON format: tasks (list of strings), unsure (True/False), msg (string).

Examples:
Input: Add a task to study ML and delete my gym task
Output: {{ "tasks": ["Add a task to study ML", "Delete my gym task"], "unsure": False, "msg": "" }}

Input: Plan my day and optimize it for productivity
Output: {{ "tasks": ["Plan my day and optimize it for productivity"], "unsure": False, "msg": "" }}

Input: Prepare me for an interview and guide me step by step
Output: {{ "tasks": ["Prepare me for an interview and guide me step by step"], "unsure": False, "msg": "" }}

Input: Add a task to study ML, delete my gym task, and move my meeting to Monday
Output: {{ "tasks": ["Add a task to study ML", "Delete my gym task", "Move my meeting to Monday"], "unsure": False, "msg": "" }}

Always respond ONLY with JSON in the above format. Do NOT add extra text.
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

    return response

print(split_tasks("Enter your task :",1))