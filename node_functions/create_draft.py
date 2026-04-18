from langchain_core.messages import ToolMessage
from langchain.tools import tool, ToolRuntime
from db.queries import insert_draft
from schemas.schemas import DraftSchema

@tool(args_schema = DraftSchema)
def create_draft(title:str, text:str, runtime:ToolRuntime):
    """
    This is the tool that stores draft in the database
    """

    print("Using create draft tool...")
    
    draft = {
        'title':title,
        'text':text
    }

    isAdded = insert_draft(draft)

    content = "Could not add draft"

    if isAdded:
        content = draft

    return ToolMessage(
        content=f"Draft successfully added. Draft data : {content}",
        tool_name="create_draft",
        tool_call_id=runtime.tool_call_id
    ) 