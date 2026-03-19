from langchain_ollama import ChatOllama
from schemas.intent_schema import IntentSchema

intent_llm = ChatOllama(model="qwen2.5:1.5b")
intent_classification_model = intent_llm.with_structured_output(IntentSchema)