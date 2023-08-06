from pydantic import BaseModel


class StaticAction(BaseModel):
    action_type: str
    link_url: str | None
