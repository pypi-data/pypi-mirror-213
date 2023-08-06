from pydantic import BaseModel

from ui.common.Button import Button
from ui.header.ContextMenuItem import ContextMenuItem


class Header(BaseModel):
    title: str
    subtitle: str | None
    context_menu: list[ContextMenuItem] | None
    buttons: list[Button] | None

