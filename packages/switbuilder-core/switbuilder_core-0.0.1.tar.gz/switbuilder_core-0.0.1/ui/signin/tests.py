import unittest

from ui.common.Button import Button
from ui.common.Icon import Icon
from ui.common.StaticAction import StaticAction
from ui.signin.IntegratedService import IntegratedService
from ui.signin.SignInPage import SignInPage


class Test(unittest.TestCase):
    def test_valid_signin(self):
        given = {
            "type": "sign_in_page",
            "integrated_service": {
                "icon": {
                    "type": "image",
                    "image_url": "http://example.com",
                    "alt": "string",
                }
            },
            "title": "Connect to Google Calendar",
            "description": "Integrate your Google Calendar to manage events and tasks within Swit.",
            "button": {
                "type": "button",
                "label": "string",
                "style": "secondary",
                "disabled": False,
                "action_id": "action_01",
                "static_action": {
                    "action_type": "open_link",
                    "link_url": "http://example.com"
                },
                "icon": {
                    "type": "image",
                    "image_url": "http://example.com",
                    "alt": "string",
                }
            }
        }

        sign_in_page = SignInPage(
            type="sign_in_page",
            integrated_service=IntegratedService(
                icon=Icon(
                    type='image',
                    image_url='http://example.com',
                    alt='string'
                )
            ),
            title="Connect to Google Calendar",
            description="Integrate your Google Calendar to manage events and tasks within Swit.",
            button=Button(
                label='string',
                type='button',
                style="secondary",
                disabled=False,
                action_id="action_01",
                icon=Icon(
                    type='image',
                    image_url='http://example.com',
                    alt='string'
                ),
                static_action=StaticAction(
                    action_type='open_link',
                    link_url='http://example.com'
                )
            )
        )

        self.assertEqual(given, sign_in_page.dict(exclude_none=True))
