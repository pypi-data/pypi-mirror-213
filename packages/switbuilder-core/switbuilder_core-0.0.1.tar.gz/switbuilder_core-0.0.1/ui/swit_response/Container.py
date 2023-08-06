from pydantic import BaseModel


class Container(BaseModel):
    type: str = "container"
    elements: list[object]
