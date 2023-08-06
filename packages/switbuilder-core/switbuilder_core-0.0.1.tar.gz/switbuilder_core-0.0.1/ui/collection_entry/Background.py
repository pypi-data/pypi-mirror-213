from pydantic import BaseModel


class Background(BaseModel):
    color: str
