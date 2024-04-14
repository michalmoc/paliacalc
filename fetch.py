from model.item import Item
from model.recipe import Recipe
from model.tag import Tag
from remote.paliapedia_api import PaliaApi


def fetch_item(api: PaliaApi, key: str) -> Item:
    return Item(api.get_item(key))


def fetch_tag(api: PaliaApi, key: str) -> Tag:
    return Tag(api.get_tag(key))


def fetch_recipe(api: PaliaApi, key: str) -> Recipe:
    return Recipe(api.get_recipe(key))