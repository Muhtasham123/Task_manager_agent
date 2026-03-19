from states.tm_state import TaskManagerState
from langchain_core.messages import SystemMessage, HumanMessage
from models.task_generation_model import generation_model

def optimize_task(state : TaskManagerState):
    task = state['task']
    user_input = state['user_input']
    missing_info = state['missing_info']
    feedback = state['feedback']

    system_message = f"""
    You are a task completion assistant.

    You are given:
    - A partially filled task
    - Missing fields
    - User input
    - Feedback

    Your job:
    - Fill ONLY the missing fields
    - Do NOT change correct existing fields
    - Keep values concise and consistent

    Return ONLY valid JSON:
    {{
      "title": "",
      "description": "",
      "category": "",
      "priority": "",
      "due_time": ""
    }}

    Task:
    {task}

    Missing Fields:
    {missing_info}

    User Input:
    {user_input}

    Feedback:
    {feedback}
    """

    messages = [
        SystemMessage(system_message),
    ]

    task = generation_model.invoke(messages).model_dump()

    return {
        'task':task,
        'iterations': state['iterations'] + 1
    }
    