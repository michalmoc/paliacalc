from dataclasses import dataclass
from functools import cached_property

from model.item import Item


@dataclass
class InputItem:
    key: str


@dataclass
class InputTag:
    key: str


class Recipe:
    def __init__(self, json):
        self.json = json['recipe']

    @cached_property
    def output_amount(self) -> int:
        return self.json['outputQuantity']

    @cached_property
    def output_item(self) -> Item:
        return Item({'item': self.json['outputItem']})

    @cached_property
    def craft_time_seconds(self) -> int:
        return self.json['craftTime']

    @cached_property
    def inputs(self) -> [(int, str)]:
        def ingr(i):
            if i['type'] == 'tag':
                return InputTag(key=i['tag']['key'])
            else:
                return InputItem(key=i['item']['key'])

        return [(i['quantity'], ingr(i)) for i in self.json['ingredients']]
