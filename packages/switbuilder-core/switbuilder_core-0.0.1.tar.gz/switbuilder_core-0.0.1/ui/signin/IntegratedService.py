from pydantic import BaseModel

from ui.common.Icon import Icon


class IntegratedService(BaseModel):
    icon: Icon
