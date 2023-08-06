import unittest

from ui.collection_entry.Background import Background
from ui.collection_entry.CollectionEntry import CollectionEntry
from ui.collection_entry.MetadataItem import MetadataItem
from ui.collection_entry.TextContent import TextContent
from ui.collection_entry.TextSection import TextSection
from ui.collection_entry.TextStyle import TextStyle
from ui.common.StaticAction import StaticAction


class Test(unittest.TestCase):
    def test_valid_collection_entry(self):
        given = {
            "type": "collection_entry",
            "text_sections": [
                {
                    "text": {
                        "type": "text",
                        "content": "Subject line",
                        "style": {
                            "bold": True,
                            "color": "gray800",
                            "size": "large",
                            "max_lines": 1
                        }
                    },
                    "metadata_items": [
                        {
                            "type": "tag",
                            "content": "label",
                            "style": {
                                "color": "primary",
                                "shape": "rounded"
                            }
                        },
                        {
                            "type": "subtext",
                            "content": "09:00AM"
                        },
                        {
                            "type": "image",
                            "image_url": "./assets/builder_logo.png"
                        }
                    ]
                },
                {
                    "text": {
                        "type": "text",
                        "content": "Subject line",
                        "style": {
                            "bold": True,
                            "color": "gray800",
                            "size": "large",
                            "max_lines": 1
                        }
                    }
                }
            ],
            "vertical_alignment": "middle",
            "background": {
                "color": "lightblue"
            },
            "action_id": "action_collection_entry",
            "static_action": {
                "action_type": "open_link",
                "link_url": "https://swit.io"
            },
            "draggable": False
        }
        # given =
        # given = {
        #     "type": "collection_entry",
        #     "text_sections": [
        #         {
        #             "text": {
        #                 "type": "text",
        #                 "content": "Subject line",
        #                 "style": {
        #                     "bold": True,
        #                     "color": "gray800",
        #                     "size": "large",
        #                     "max_lines": 1
        #                 }
        #             },
        #             "metadata_items": [
        #                 {
        #                     "type": "tag",
        #                     "content": "label",
        #                     "style": {
        #                         "color": "primary",
        #                         "shape": "rounded"
        #                     }
        #                 },
        #                 {
        #                     "type": "subtext",
        #                     "content": "09:00AM"
        #                 },
        #                 {
        #                     "type": "image",
        #                     "image_url": "./assets/builder_logo.png"
        #                 }
        #             ]
        #         },
        #         {
        #             "text": {
        #                 "type": "text",
        #                 "content": "Subject line",
        #                 "style": {
        #                     "bold": True,
        #                     "color": "gray800",
        #                     "size": "large",
        #                     "max_lines": 1
        #                 }
        #             },
        #             "metadata_items": [
        #                 {
        #                     "type": "tag",
        #                     "content": "label",
        #                     "style": {
        #                         "color": "primary",
        #                         "shape": "rounded"
        #                     }
        #                 },
        #                 {
        #                     "type": "subtext",
        #                     "content": "09:00AM"
        #                 },
        #                 {
        #                     "type": "image",
        #                     "image_url": "./assets/builder_logo.png"
        #                 }
        #             ]
        #         },
        #     ],
        #     "start_section": {
        #         "type": "image",
        #         "image_url": "./assets/builder_logo.png",
        #         "alt": "alt string",
        #         "style": {
        #             "size": "medium"
        #         }
        #     },
        #     "vertical_alignment": "middle",
        #     "background": {
        #         "color": "lightblue"
        #     },
        #     "action_id": "action_collection_entry",
        #     "static_action": {
        #         "action_type": "open_link",
        #         "link_url": "https://swit.io"
        #     },
        #     "draggable": False
        # }

        text_section1 = TextSection(
            text=TextContent(
                content="Subject line",
                style=TextStyle(
                    bold=True,
                    color="gray800",
                    size="large",
                    max_lines=1
                )
            ),
            metadata_items=[
                MetadataItem(
                    type="tag",
                    content="label",
                    style={
                        "color": "primary",
                        "shape": "rounded"
                    }
                ),
                MetadataItem(
                    type="subtext",
                    content="09:00AM"
                ),
                MetadataItem(
                    type="image",
                    image_url="./assets/builder_logo.png"
                ),
            ]
        )

        text_section2 = TextSection(
            text=TextContent(
                content="Subject line",
                style=TextStyle(
                    bold=True,
                    color="gray800",
                    size="large",
                    max_lines=1
                )
            ),
        )

        c = CollectionEntry(
            text_sections=[text_section1, text_section2],
            vertical_alignment="middle",
            background=Background(color="lightblue"),
            action_id="action_collection_entry",
            static_action=StaticAction(
                action_type="open_link",
                link_url="https://swit.io"
            ),
            draggable=False
        )

        self.assertEqual(given, c.dict(exclude_none=True))
