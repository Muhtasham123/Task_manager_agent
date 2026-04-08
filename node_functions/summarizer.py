from states.tm_state import TaskManagerState
from langchain_core.messages import HumanMessage, SystemMessage
from modals.summarization_modal import summarization_modal

def summarize_chat(state:TaskManagerState):
    #Extracting system message to preserve it from trimming
    system_message = state['messages'][0]

    #keep recent 100 messages  
    recent_messages = state["messages"][-100:]

    summary = state['summary']

    prompt = ""
    if not summary:
        prompt = f"Summarize the conversation above."
    else:
        prompt = (
            f"Existing summary:\n{summary}\n\n"
            "Extend the summary using the new conversation above."
        )
    
    messages_for_summary = state["messages"][1:-100] + [HumanMessage(content=prompt)]
    new_summary = summarization_modal.invoke(messages_for_summary)
    new_messages = [system_message, SystemMessage(content=f"Summary of conversation so far:\n{new_summary}")] + recent_messages

    return{
        'new_summary' : new_summary.content,
        'new_messages' : new_messages
    } 