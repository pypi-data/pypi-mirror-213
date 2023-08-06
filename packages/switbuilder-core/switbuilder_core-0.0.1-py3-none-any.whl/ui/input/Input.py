from pydantic import BaseModel


class Input(BaseModel):
    type: str = 'text_input'
    action_id: str
    placeholder: str
    trigger_on_input: bool
    value: str | None
