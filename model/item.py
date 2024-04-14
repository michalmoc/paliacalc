from functools import cached_property


class Item:
    def __init__(self, json):
        self.json = json['item']

    @cached_property
    def name(self) -> str:
        return self.json['name']

    @cached_property
    def focus(self) -> int | None:
        if 'consumeRewards' in self.json:
            try:
                return next(r for r in self.json['consumeRewards'] if r['type'] == 'Focus')['amount']
            except StopIteration:
                return None
        else:
            return None

    @cached_property
    def buy_cost(self) -> int | None:
        if 'cost' in self.json and self.json['cost']['currency']['name'] == 'Gold':
            return self.json['cost']['amount']
        return None

    @cached_property
    def sell_value(self) -> int | None:
        if 'value' in self.json and self.json['value']['currency']['name'] == 'Gold':
            return self.json['value']['amount']
        return None

    @cached_property
    def type(self) -> str | None:
        if 'type' in self.json:
            return self.json['type']
        return None

    @cached_property
    def recipe(self) -> str | None:
        if 'recipes' in self.json['sources']:
            assert len(self.json['sources']['recipes']) == 1
            return self.json['sources']['recipes'][0]['key']
        return None

    def is_source(self) -> bool:
        # exceptional case, oyster meat is not directly gathered but opened from oyster
        return self.type in {'Vegetable', 'Fruit',
                             'Crop'} or self.is_gatherable() or self.name == "Oyster Meat"

    def is_gatherable(self) -> bool:
        if 'gatherables' not in self.json['sources']:
            return False
        return any(
            (('type' not in source or source['type'] != 'Treasure') and 'Rummage Pile' not in source['name'] for source
             in
             self.json['sources']['gatherables']))