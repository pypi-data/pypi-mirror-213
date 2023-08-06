from enum import Enum

from pydantic import BaseModel

from ui.swit_response.AttachmentView import AttachmentView
from ui.swit_response.View import View


class ViewCallbackType(str, Enum):
    update = "views.update"
    initialize = "views.initialize"
    open = "views.open"
    push = "views.push"
    close = "views.close"


class AttachmentCallbackType(str, Enum):
    share_channel = "attachments.share.channel"


class ViewResponse(BaseModel):
    callback_type: ViewCallbackType
    new_view: View


class AttachmentResponse(BaseModel):
    callback_type: AttachmentCallbackType
    attachments: AttachmentView


class SwitResponse(BaseModel):
    callback_type: ViewCallbackType | AttachmentCallbackType
    new_view: View | None
    attachments: AttachmentView | None
    reference_view_id: str | None
