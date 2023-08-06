from pydantic import BaseModel


class TextStyle(BaseModel):
    bold: bool = False
    color: str
    size: str
    max_lines: int
