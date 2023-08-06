from pydantic import BaseModel


class MetadataItem(BaseModel):
    type: str
    content: str | None
    style: dict | None
    image_url: str | None
