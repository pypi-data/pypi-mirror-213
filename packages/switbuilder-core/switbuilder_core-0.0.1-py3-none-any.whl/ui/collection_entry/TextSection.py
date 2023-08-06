from pydantic import BaseModel

from ui.collection_entry.MetadataItem import MetadataItem
from ui.collection_entry.TextContent import TextContent


class TextSection(BaseModel):
    text: TextContent
    metadata_items: list[MetadataItem] | None
