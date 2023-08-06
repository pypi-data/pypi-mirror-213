from pydantic import BaseModel


class ContextMenuItem(BaseModel):
    label: str
    action_id: str
