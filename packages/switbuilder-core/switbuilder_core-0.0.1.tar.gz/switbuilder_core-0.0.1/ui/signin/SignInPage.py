from pydantic import BaseModel

from ui.common.Button import Button
from ui.signin.IntegratedService import IntegratedService


class SignInPage(BaseModel):
    id: str | None = None
    type: str = "sign_in_page"
    integrated_service: IntegratedService
    title: str
    description: str
    button: Button
