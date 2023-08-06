from pydantic import BaseModel


class Option(BaseModel):
    label: str
    action_id: str
    # static_action: Dict[str, str] | None