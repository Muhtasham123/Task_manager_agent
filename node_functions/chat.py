from states.tm_state import TaskManagerState
from langchain_core.messages import HumanMessage
from modals.chat_modal import modal 

def chat(state : TaskManagerState):
    """LLM node that may answer or request a tool call"""

    messages = state['messages']

    response = modal.invoke(messages)

    return {
        'messages':response
    }