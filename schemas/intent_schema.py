from pydantic import BaseModel, Field
from typing import Literal 

class IntentSchema(BaseModel):
    intent:Literal['create_task', 'update_task', 'delete_task', 'other'] = Field(description="Intent of the user")