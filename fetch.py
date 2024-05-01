from model.item import Item
from model.recipe import Recipe
from model.tag import Tag
from remote.paliapedia_api import PaliaApi


def fetch_item(api: PaliaApi, key: str) -> Item:
    if key == 'mineral-glass-pane':  # bug in paliapedia
        return Item({'item': {
            'name': 'Glass Pane',
            'sources':{
                'recipes': [
                    {'key': 'FIX-glasspane'}
                ]
            }
        }})
    return Item(api.get_item(key))


def fetch_tag(api: PaliaApi, key: str) -> Tag:
    return Tag(api.get_tag(key))


def fetch_recipes(api: PaliaApi, categories: str | list[str]) -> Tag:
    if type(categories) is str:
        return Tag(api.get_recipes(categories))
    else:
        return sum((fetch_recipes(api, category) for category in categories), Tag([]))


def fetch_recipe(api: PaliaApi, key: str) -> Recipe:
    if key == 'FIX-glasspane':  # bug in paliapedia
        return Recipe({'recipe': {
            'outputItem': {
                'name': 'Glass Pane',
                'value': {'currency': {'key': 'vital-coins', 'name': 'Gold'}, 'amount': 13}},
            'outputQuantity': 1,
            'ingredients': [
                {'type':'item', 'item': {'key': 'mineral-rock-stone'}, 'quantity': 10}
            ],
            'craftTime': 8 * 60
        }})

    return Recipe(api.get_recipe(key))
