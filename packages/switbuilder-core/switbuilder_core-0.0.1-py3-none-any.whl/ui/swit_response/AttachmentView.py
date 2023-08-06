from pydantic import BaseModel

from ui.header.Header import Header
from ui.swit_response.Body import Body
from ui.swit_response.Footer import Footer


class AttachmentView(BaseModel):
    state: str | bytes
    header: Header
    footer: Footer | None
    body: Body

