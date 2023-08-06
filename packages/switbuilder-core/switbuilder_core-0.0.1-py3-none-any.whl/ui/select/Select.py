from pydantic import BaseModel

from ui.select.Option import Option
from ui.select.Style import Style


class Select(BaseModel):
    type: str = 'select'
    placeholder: str | None
    trigger_on_input: bool
    value: list[str] | None
    options: list[Option]
    # target: str | None
    # multiselect: bool = False
    style: Style | None = None
