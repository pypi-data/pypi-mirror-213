from pydantic import BaseModel


class StartSection(BaseModel):
    type: str
    image_url: str
    alt: str
    style: dict
