from langchain_ollama import ChatOllama
from schemas.task_schema import TaskSchema

generation_llm = ChatOllama(model="qwen2.5:1.5b")
generation_model = generation_llm.with_structured_output(TaskSchema)