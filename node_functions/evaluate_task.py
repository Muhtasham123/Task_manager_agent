from states.tm_state import TaskManagerState
from langchain_core.messages import SystemMessage, HumanMessage
from models.task_evaluation_model import evaluation_model

def evaluate_task(state : TaskManagerState):
    task = state['task']
    user_input = state['user_input']
    system_message = f"""
    You are a task validation assistant.

    Check the task for:
    1. Missing or empty fields:
       title, description, category, priority, due_time

    2. Invalid values based on user input.

    Return ONLY JSON:
    {{
      "status": "optimized" OR "needs_optimization",
      "missing_fields": [],
      "invalid_fields": [],
      "feedback": ""
    }}

    Rules:
    - missing_fields: fields that are missing or empty
    - invalid_fields: fields that do not match user input
    - feedback: short (1–2 lines)

    Task:
    {task}

    User Input:
    {user_input}
    """

    messages = [
        SystemMessage(system_message),
    ]

    response = evaluation_model.invoke(messages)

    return {
        'feedback':response.feedback,
        'task_status':response.status,
        'missing_info':response.missing_info
    }