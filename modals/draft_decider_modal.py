from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from schemas.schemas import DraftDeciderSchema

load_dotenv()
                       
initial_modal = ChatOpenAI(
    model="gpt-4o-mini",
    temperature = 0
)

modal = initial_modal.with_structured_output(DraftDeciderSchema)