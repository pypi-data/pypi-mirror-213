from pydantic import BaseModel

from ui.collection_entry.Background import Background
from ui.collection_entry.StartSection import StartSection
from ui.collection_entry.TextSection import TextSection
from ui.common.StaticAction import StaticAction


class CollectionEntry(BaseModel):
    type: str = "collection_entry"
    text_sections: list[TextSection]
    start_section: StartSection | None
    vertical_alignment: str
    background: Background
    action_id: str | None
    static_action: StaticAction | None
    draggable: bool
