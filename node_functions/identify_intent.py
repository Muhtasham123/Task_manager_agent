from states.tm_state import TaskManagerState
from langchain_core.messages import SystemMessage, HumanMessage
from models.intent_classification_model import intent_classification_model

def identify_intent(state : TaskManagerState):
    user_input = state['user_input']

    messages = [
        SystemMessage("You need to classify intent of user based on user input.\n possible intents : \ncreate_task\nupdate_task\ndelete_task\nother"),

        HumanMessage(user_input)
    ]

    intent = intent_classification_model.invoke(messages).intent

    return {
        'intent':intent
    }
    