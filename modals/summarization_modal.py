from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

summarization_modal = ChatOpenAI(
    model="gpt-4o-mini",
    temperature = 0
)