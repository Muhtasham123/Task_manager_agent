from states.tm_state import TaskManagerState
from modals.draft_modal import modal
from prompt import draft_prompt
from langchain_core.messages import SystemMessage, HumanMessage

def draft(state:TaskManagerState):
    print("Executing Draft node...")
    user_query = state['user_query']

    # Exracting messages except system messages
    message_history = [message for message in state['messages'] if not isinstance(message,SystemMessage)]

    # Putting draft decider system message on first index
    system_message = SystemMessage(content=draft_prompt)

    message_history.insert(0, system_message)

    response = modal.invoke(message_history + [HumanMessage(content=user_query)])

    print("Draft response : ", response)
    return{
        'messages':[response]
    }