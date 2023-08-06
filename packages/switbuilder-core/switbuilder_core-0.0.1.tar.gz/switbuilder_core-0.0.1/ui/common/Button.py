from typing import Optional

from pydantic import BaseModel

from ui.common.Icon import Icon
from ui.common.StaticAction import StaticAction


class Button(BaseModel):
    id: Optional[str] = None
    type: str = "button"
    label: str | None = None
    style: str | None = None
    disabled: bool | None = None
    action_id: str | None = None
    static_action: StaticAction | None = None
    icon: Icon | None = None
