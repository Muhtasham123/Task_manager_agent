from states.tm_state import TaskManagerState
from langchain_core.messages import SystemMessage, ToolMessage, AIMessage, HumanMessage
from langchain_core.messages.utils import trim_messages, count_tokens_approximately
from modals.chat_modal import modal 
import json


MAX_TOKENS = 100000

def chat(state : TaskManagerState):
    """LLM node that may answer or request a tool call"""

    print("Thinking....")

    #Extracting system message to preserve it from trimming
    system_message = state['messages'][0]
    other_messages = state["messages"][1:]

    #Trimming messages to maintain the context window
    messages = trim_messages(
        other_messages,
        strategy="last",                      
        token_counter=count_tokens_approximately,
        max_tokens=MAX_TOKENS
    )

    messages = [system_message] + messages
    print('Current Token Count ->', count_tokens_approximately(messages=messages))
    last_message = messages[-1] if messages else None

    #Adding last approval msg and human response to state in case of update and delete
    ai_message = ""
    human_message = ""

    if (last_message and 
    isinstance(last_message, ToolMessage) and 
    (last_message.name == "delete_task" or last_message.name == 'update_task')):
        
        tool_message = json.loads(last_message.content)
        ai_message = tool_message['ai_message']
        human_message = tool_message['human_message']

    #Enforcing llm to use single tool per response adn retrying on multiple tools
    for try_no in range(1, 3):
        print("Try no : ", try_no)
        response = modal.invoke(messages)

        if len(response.tool_calls) > 1:
            messages.append(SystemMessage("You are only allowed to call ONE tool per response. Try again"))
        else:
            break

    print(response)

    iterations = state.get('iterations', 0) + 1
    return {
        **state,
        'messages':[AIMessage(content=ai_message)]+[HumanMessage(content=human_message)]+[response],
        'iterations':iterations
    }