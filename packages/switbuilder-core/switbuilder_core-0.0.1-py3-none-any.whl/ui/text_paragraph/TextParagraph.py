from pydantic import BaseModel


class TextParagraph(BaseModel):
    type: str = "text"
    markdown: bool = False
    content: str
