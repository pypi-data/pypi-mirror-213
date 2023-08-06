from pydantic import BaseModel
from enum import Enum

from ui.common.StaticAction import StaticAction


class FileType(str, Enum):
    image = "image"
    video = "video"
    document = "document"
    pdf = "pdf"
    presentation = "presentation"
    spreadsheet = "spreadsheet"
    archive = "archive"
    psd = "psd"
    ai = "ai"
    other = "other"


class File(BaseModel):
    type: str = "file"
    file_type: FileType
    file_size: int
    file_name: str
    action_id: str | None
    static_action: StaticAction | None
