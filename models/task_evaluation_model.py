from langchain_ollama import ChatOllama
from schemas.evaluation_schema import EvaluationSchema

evaluation_llm = ChatOllama(model="phi3:mini")
evaluation_model = evaluation_llm.with_structured_output(EvaluationSchema)