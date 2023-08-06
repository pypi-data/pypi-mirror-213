import unittest

from ui.select.Option import Option
from ui.select.Select import Select


class Test(unittest.TestCase):
    def test_valid_select(self):
        given = {
            "type": "select",
            "placeholder": "Objects",
            "trigger_on_input": True,
            "value": [
                "sobjectSelected-all"
            ],
            "options": [
                {
                    "label": "all",
                    "action_id": "sobjectSelected-all"
                },
                {
                    "label": "Accounts",
                    "action_id": "sobjectSelected-Account"
                },
                {
                    "label": "Contacts",
                    "action_id": "sobjectSelected-Contact"
                }
            ]
        }

        select = Select(
            placeholder="Objects",
            trigger_on_input=True,
            value=[
                "sobjectSelected-all"
            ],
            options=[
                Option(label="all", action_id="sobjectSelected-all"),
                Option(label="Accounts", action_id="sobjectSelected-Account"),
                Option(label="Contacts", action_id="sobjectSelected-Contact"),
            ],
        )

        self.assertEqual(given, select.dict(exclude_none=True))
