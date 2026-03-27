from states.tm_state import TaskManagerState
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from modals.create_task_modal import modal
from utils.parser import due_time_parser
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from db.queries import insert_task

@tool
def create_task(task_statement : str, runtime : ToolRuntime) -> Command:

    """LLM node for extracting task as JSON"""

    system_message = f"""
    You are a task extraction assistant.

    Extract the following fields from the user input:
    - title (3–6 words)
    - description (1 short sentence)
    - category (work, study, personal, health, other)
    - priority (low, medium, high)
    - due_time (provided by user in string like next week, tomorrow etc)

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

        HumanMessage(task_statement)
    ]

    task = modal.invoke(messages).model_dump()

    date_str = task['due_time']

    parsed_date = due_time_parser(date_str)

    task['due_time'] = parsed_date

    insert_task(task)

    tool_message = ToolMessage(
        content=str(task),
        tool_name="create_task",
        tool_call_id=runtime.tool_call_id
    )

    return Command(update={"task":task, "messages": [tool_message]})
    