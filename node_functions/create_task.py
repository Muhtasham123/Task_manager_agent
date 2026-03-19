from states.tm_state import TaskManagerState
from langchain_core.messages import SystemMessage, HumanMessage
from models.task_generation_model import generation_model

def create_task(state : TaskManagerState):
    user_input = state['user_input']

    system_message = f"""
    You are a task extraction assistant.

    Extract the following fields from the user input:
    - title (3–6 words)
    - description (1 short sentence)
    - category (work, study, personal, health, other)
    - priority (low, medium, high)
    - due_time

    Rules:
    - Infer category and priority if missing.
    - If due_time is not mentioned, return null.
    - Keep output concise.

    Return ONLY valid JSON:
    {{
      "title": "",
      "description": "",
      "category": "",
      "priority": "",
      "due_time": ""
    }}
    """

    messages = [
        SystemMessage(system_message),

        HumanMessage(user_input)
    ]

    task = generation_model.invoke(messages).model_dump()

    return {
        'task':task
    }
    