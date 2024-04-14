import logging

from find_creation_cost import find_item_creation_cost
from model.item import Item
from model.tag import Tag
from remote.paliapedia_api import PaliaApi


def check_focus_value(api: PaliaApi, item_key: str):
    item = Item(api.get_item(item_key))

    cost = find_item_creation_cost(api, item)
    focus = item.focus

    if cost is not None and focus is not None:
        return item.name, cost / focus
    return None


def main():
    logging.basicConfig(level=logging.WARNING)
    api = PaliaApi()

    foods = Tag(api.get_tag('Item.Consumable'))
    results = []
    for food in foods.options:
        result = check_focus_value(api, food)
        if result is not None:
            results.append(result)

    results.sort(key=lambda e: e[1], reverse=True)
    for name, value in results:
        print(f"{name}\t: \t{value:.2f} gp/f")


if __name__ == '__main__':
    main()
