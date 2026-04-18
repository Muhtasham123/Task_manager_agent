import dateparser
from langchain_core.documents import Document
from states.tm_state import TaskManagerState

def due_time_parser(date_str):

    parsed_date = dateparser.parse(
        date_str, 
        settings={"TIMEZONE": "Asia/Karachi", "RETURN_AS_TIMEZONE_AWARE": True}
    )

    if parsed_date is None:
        return None
    else:
        return parsed_date.isoformat()
    
def format_memories(memories):
    return "\n".join([f"- {m.value['data']}" for m in memories])

def resolve_draft_decision(state: TaskManagerState):
    if state['draft_decision'] == 'need_draft':
        return 'need_draft'
    else:
        return 'not_need_draft'
    

def tool_router(state: TaskManagerState):
    """
    Decides whether we need tools or can directly go to draft_decider.
    """

    messages = state["messages"]
    last_msg = messages[-1]

    # If LLM requested tools → must go to tools node
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "need_tools"

    # Otherwise safe to proceed
    return "not_need_tools"

