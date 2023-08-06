import unittest

from ui.input.Input import Input


class Test(unittest.TestCase):
    def test_valid_input(self):
        _input = Input(
            type='text_input',
            action_id='searchRecord',
            placeholder='Search',
            trigger_on_input=True
        )

        given = {'type': 'text_input',
                 'action_id': 'searchRecord',
                 'placeholder': 'Search',
                 'trigger_on_input': True}

        self.assertEqual(given, _input.dict(exclude_none=True))
