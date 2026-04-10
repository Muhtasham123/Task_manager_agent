from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

class MemoryItemSchema(BaseModel):
    is_new:bool
    memory_item:str = Field(description="Text of a memory")

class MemorySchema(BaseModel):
    should_write:bool
    memories:List[MemoryItemSchema] = Field(description="list of memory items to be stored")

modal = ChatOpenAI(
    model="gpt-4o-mini",
    temperature = 0
)

memorization_modal = modal.with_structured_output(MemorySchema)