import unittest

from ui.common.Button import Button
from ui.common.Icon import Icon
from ui.common.StaticAction import StaticAction
from ui.header.ContextMenuItem import ContextMenuItem
from ui.header.Header import Header


class Test(unittest.TestCase):
    def test_valid_header(self):
        given = {
            "title": "This is a view title",
            "subtitle": "Add a subtitle if needed",
            "context_menu": [
                {
                    "label": "Menu item 1",
                    "action_id": "2fc5573a-c439-4131-9c82-6ed78c1f1758"
                },
                {
                    "label": "Menu item 2",
                    "action_id": "340d4ae1-0cb2-42c7-8880-4b5c2aed0f2d"
                },
                {
                    "label": "Menu item 3",
                    "action_id": "449fec68-ad54-4ee8-aa29-1c56957868c7"
                }
            ],
            "buttons": [
                {
                    "type": "button",
                    "icon": {
                        "type": "image",
                        "image_url": "https://swit.io/assets/images/lib/emoji/apple-64/1f609.png",
                        "alt": "Header button icon"
                    },
                    "static_action": {
                        "action_type": "open_link",
                        "link_url": "https://swit.io"
                    }
                }
            ]
        }

        header = Header(
            title='This is a view title',
            subtitle='Add a subtitle if needed',
            context_menu=[
                ContextMenuItem(label='Menu item 1', action_id='2fc5573a-c439-4131-9c82-6ed78c1f1758'),
                ContextMenuItem(label='Menu item 2', action_id='340d4ae1-0cb2-42c7-8880-4b5c2aed0f2d'),
                ContextMenuItem(label='Menu item 3', action_id='449fec68-ad54-4ee8-aa29-1c56957868c7')
            ],
            buttons=[
                Button(
                    type='button',
                    icon=Icon(
                        type='image',
                        image_url='https://swit.io/assets/images/lib/emoji/apple-64/1f609.png',
                        alt='Header button icon'
                    ),
                    static_action=StaticAction(
                        action_type='open_link',
                        link_url='https://swit.io'
                    )
                )
            ])

        self.assertEqual(given, header.dict(exclude_none=True))
