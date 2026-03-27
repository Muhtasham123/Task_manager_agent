from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from schemas.task_schema import TaskSchema

load_dotenv()

initial_modal = ChatOpenAI(
    model="gpt-4o-mini",
    temperature = 0
)

modal = initial_modal.with_structured_output(TaskSchema)