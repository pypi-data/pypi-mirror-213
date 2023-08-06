from pydantic import BaseModel


class Image(BaseModel):
    type: str = "image"
    image_url: str
    alt: str = ""
