from pydantic import BaseModel

from ui.common.Button import Button


class Footer(BaseModel):
    buttons: list[Button]
