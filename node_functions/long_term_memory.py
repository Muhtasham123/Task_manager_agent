from states.tm_state import TaskManagerState
from langgraph.store.base import BaseStore
from prompt import memory_system_prompt, system_prompt
from modals.memory_extractor_model import memorization_modal
from namespace import namespace
from langchain_core.messages import SystemMessage
import uuid
from utils.functions import format_memories

def memory_handler(state:TaskManagerState,store:BaseStore):
    #getting user query from messages
    query = state['messages'][-1].content

    #getting current 5 most relevant memmories of a user
    current_memory_items = store.search(namespace, query=query, limit=5)

    #modifying system prompt if memories exist
    formated_memories = format_memories(current_memory_items)
    if current_memory_items:
        modified_system_prompt = SystemMessage(system_prompt.format(user_details_content=formated_memories))

        state['messages'][0] = modified_system_prompt

    #giving current memmories and query to llm to extract new memories
    new_memories = memorization_modal.invoke(
        [
            SystemMessage(content=memory_system_prompt.format(user_details_content=formated_memories)),
            {"role": "user", "content": query},
        ]
    )

    print("New Memories extracted by modal : ", new_memories)

    #Checking if memory is worthy to be written in store
    if new_memories.should_write:
        for memory in new_memories.memories:
            #checking if memory is new or already exists in store
            if memory.is_new:
                store.put(namespace, uuid.uuid4(), {"data":memory.memory_item.strip()})
    
    return {}