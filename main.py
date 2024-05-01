import logging
from logging import debug

from fetch import fetch_tag, fetch_recipes, fetch_recipe
from find_creation_cost import find_item_creation_cost, find_recipe_creation_cost
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


def calculate_focus_values(api: PaliaApi):
    """
    Return pairs (consumable name, cost in gold/focus point)
    """
    foods = fetch_tag(api, 'Item.Consumable')
    results = []
    for food in foods.options:
        result = check_focus_value(api, food)
        if result is not None:
            results.append(result)

    results.sort(key=lambda e: e[1], reverse=True)
    return results


def calculate_crafter_income(api:PaliaApi, recipe: str) -> (str, float):
    recipe = fetch_recipe(api, recipe)

    name = recipe.output_item.name
    output_value = recipe.output_item.sell_value
    input_value = find_recipe_creation_cost(api, recipe)
    time = recipe.craft_time_seconds / (60 * recipe.output_amount)

    debug(f'{name}: from {input_value} makes {output_value} in {time}min')

    value = (output_value - input_value) / time
    return name, value


def calculate_crafter_incomes(api: PaliaApi, star:bool) -> [(str, float)]:
    """
    Return pairs (consumable name, income in gold/minute)
    """
    results = []

    recipes = fetch_recipes(api, ["Product", "Seed"])
    for recipe in recipes.options:
        name, value = calculate_crafter_income(api, recipe)
        results.append((name, value * (1.5 if star else 1)))

    recipes = fetch_recipes(api, "Material")
    for recipe in recipes.options:
        name, value = calculate_crafter_income(api, recipe)
        results.append((name, value))

    for recipe in ['r-material-fabric', 'r-mineral-glass-bulb', 'r-material-leather', 'plank-softwood', 'brick-stone', 'FIX-glasspane']: # bug in paliapedia
        name, value = calculate_crafter_income(api, recipe)
        results.append((name, value))

    results.sort(key=lambda e: e[1], reverse=False)
    return results


def print_table(headers: (str, str), items: [(str, float)]):
    print('| {} | {} |'.format(*headers))
    print('|---|---|')
    for name, value in items:
        print(f"| {name} | {value:.2f} |")
    print("")


def main():
    logging.basicConfig(level=logging.DEBUG)
    api = PaliaApi()

    crafter_incomes = calculate_crafter_incomes(api, star=True)
    print_table(('Product', 'Income per minute'), crafter_incomes)

    # focus_values = calculate_focus_values(api)
    # print_table(('Food', 'Focus cost'), focus_values)


if __name__ == '__main__':
    main()
