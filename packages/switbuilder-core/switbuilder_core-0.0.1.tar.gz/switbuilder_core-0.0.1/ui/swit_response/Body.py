from typing import Any

from pydantic import BaseModel

from ui.collection_entry.CollectionEntry import CollectionEntry
from ui.common.Button import Button
from ui.divider.Divider import Divider
from ui.file.File import File
from ui.html_frame.HtmlFrame import HtmlFrame
from ui.image.Image import Image
from ui.input.Input import Input
from ui.select.Select import Select
from ui.signin.SignInPage import SignInPage
from ui.text_paragraph.TextParagraph import TextParagraph

ElementType = CollectionEntry | Button | Divider | File | HtmlFrame | Input | Select | SignInPage | TextParagraph | Image


def contain_only_dict(elements_data: list[dict | ElementType]) -> bool:
    for element_data in elements_data:
        if isinstance(element_data, ElementType):
            return False

    return True


def get_element_type(element_data: dict):
    element_type_str = element_data.get('type')
    if element_type_str == 'collection_entry':
        return CollectionEntry
    elif element_type_str == 'button':
        return Button
    elif element_type_str == 'divider':
        return Divider
    elif element_type_str == 'file':
        return File
    elif element_type_str == 'html_frame':
        return HtmlFrame
    elif element_type_str == 'text_input':
        return Input
    elif element_type_str == 'select':
        return Select
    elif element_type_str == 'sign_in_page':
        return SignInPage
    elif element_type_str == 'text':
        return TextParagraph
    elif element_type_str == 'image':
        return Image
    else:
        raise ValueError(f"Unknown element type: {element_type_str}")


class Body(BaseModel):
    elements: list[ElementType]

    class Config:
        smart_union = True

    def __init__(self, **data: Any) -> None:
        elements_data = data.get('elements', [])

        if contain_only_dict(elements_data):
            elements = []
            for element_data in elements_data:
                element_type = get_element_type(element_data)
                element = element_type(**element_data)
                elements.append(element)
            super().__init__(elements=elements)
        else:
            super().__init__(**data)
