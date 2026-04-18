from states.tm_state import TaskManagerState
from modals.draft_decider_modal import modal
from prompt import draft_decider_prompt
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def draft_decider(state:TaskManagerState):
    user_query = state['user_query']
    print("user query : ",user_query)

    # Exracting messages except system messages
    message_history = [message for message in state['messages'] if not isinstance(message,SystemMessage)]

    # Putting draft decider system message on first index
    system_message = SystemMessage(content=draft_decider_prompt)

    message_history.insert(0, system_message)

    response = modal.invoke(message_history + [HumanMessage(content=user_query)])

    return{
        'draft_decision':response.need_draft,
    }