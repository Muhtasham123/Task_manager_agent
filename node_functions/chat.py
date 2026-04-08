from states.tm_state import TaskManagerState
from langchain_core.messages import SystemMessage, ToolMessage, AIMessage, HumanMessage 
from modals.chat_modal import modal 
from node_functions.summarizer import summarize_chat
import json


def chat(state : TaskManagerState):
    """LLM node that may answer or request a tool call"""

    print("Thinking....")

    #summarizing conversation
    summary = ""
    print("Total messages in state : ", len(state['messages']))
    if len(state['messages']) >= 200:
       summarized_chat = summarize_chat(state)
       state['messages'] = summarized_chat['new_messages']
       summary = summarized_chat['new_summary']
       print("Summary : ", summary)
       print("Sliced chat : ", state['messages'])

    last_message = state['messages'][-1] if state['messages'] else None

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
        response = modal.invoke(state['messages'])

        if len(response.tool_calls) > 1:
            state['messages'].append(SystemMessage("You are only allowed to call ONE tool per response. Try again"))
        else:
            break

    print(response)

    iterations = state.get('iterations', 0) + 1
    return {
        **state,
        'messages':[AIMessage(content=ai_message)]+[HumanMessage(content=human_message)]+[response],
        'summary':summary,
        'iterations':iterations
    }