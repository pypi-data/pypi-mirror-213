from pydantic import BaseModel

from ui.collection_entry.TextStyle import TextStyle


class TextContent(BaseModel):
    type: str = "text"
    content: str
    style: TextStyle | None
