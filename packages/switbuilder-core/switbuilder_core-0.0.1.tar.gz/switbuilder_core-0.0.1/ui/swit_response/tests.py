import unittest

from ui.divider.Divider import Divider
from ui.header.ContextMenuItem import ContextMenuItem
from ui.header.Header import Header
from ui.input.Input import Input
from ui.swit_response.Body import Body
from ui.swit_response.SwitResponse import SwitResponse, ViewCallbackType
from ui.swit_response.View import View
from ui.text_paragraph.TextParagraph import TextParagraph


class Test(unittest.TestCase):
    def test_valid_swit_response(self):
        header = Header(
            title='This is a view title',
            subtitle='Add a subtitle if needed',
            context_menu=[
                ContextMenuItem(label='Menu item 1', action_id='2fc5573a-c439-4131-9c82-6ed78c1f1758'),
            ],
        )

        input_ = Input(
            type='text_input',
            action_id='searchRecord',
            placeholder='Search',
            trigger_on_input=True
        )

        body = Body(
            elements=[input_]
        )

        new_view = View(
            view_id="right_panel",
            state='',
            header=header,
            body=body
        )

        swit_response = SwitResponse(
            callback_type=ViewCallbackType.update,
            new_view=new_view
        )

        given = {
            'callback_type': 'views.update',
            'new_view': {'view_id': "right_panel",
                         'state': '',
                         'header': {
                             "title": "This is a view title",
                             "subtitle": "Add a subtitle if needed",
                             "context_menu": [
                                 {
                                     "label": "Menu item 1",
                                     "action_id": "2fc5573a-c439-4131-9c82-6ed78c1f1758"
                                 },
                             ]
                         },
                         'body': {'elements': [
                             {'type': 'text_input',
                              'action_id': 'searchRecord',
                              'placeholder': 'Search',
                              'trigger_on_input': True},

                         ]}}
        }

        self.assertEqual(given, swit_response.dict(exclude_none=True))

    def test_body_serializer_deserializer(self):
        elements = [Divider(), TextParagraph(content="aaa", markdown=False)]
        body_from_instance = Body(elements=elements)

        self.assertIsInstance(body_from_instance.elements[0], Divider)
        self.assertIsInstance(body_from_instance.elements[1], TextParagraph)

        data = body_from_instance.dict()
        body_from_dict = Body(**data)

        self.assertIsInstance(body_from_dict.elements[0], Divider)
        self.assertIsInstance(body_from_dict.elements[1], TextParagraph)
