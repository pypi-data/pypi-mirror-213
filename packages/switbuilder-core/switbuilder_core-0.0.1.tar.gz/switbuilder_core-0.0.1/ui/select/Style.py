from pydantic import BaseModel


class Style(BaseModel):
    variant: str | None
