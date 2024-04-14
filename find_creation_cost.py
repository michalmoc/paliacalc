from logging import error, debug

from fetch import fetch_item, fetch_tag, fetch_recipe
from model.item import Item
from model.recipe import Recipe, InputItem, InputTag
from model.tag import Tag
from remote.paliapedia_api import PaliaApi


def find_tag_creation_cost(api: PaliaApi, tag: Tag) -> float:
    """ Cost of creating 'Any Something'. Assuming the average option. Otherwise, fish is absurd expensive. """
    result = 0
    for option in tag.options:
        item = fetch_item(api, option)
        result += find_item_creation_cost(api, item)
    return result / len(tag.options)


def find_recipe_creation_cost(api: PaliaApi, recipe: Recipe) -> float:
    """ Cost of recipe. Sum of ingredients * their amount, ultimately divided by output amount. """
    result = 0
    for (amount, ingredient) in recipe.inputs:
        if type(ingredient) is InputItem:
            item = fetch_item(api, ingredient.key)
            result += amount * find_item_creation_cost(api, item)
        elif type(ingredient) is InputTag:
            item = fetch_tag(api, ingredient.key)
            result += amount * find_tag_creation_cost(api, item)
        else:
            error(f'unknown type {type(ingredient)}')
    return result / recipe.output_amount


def find_item_creation_cost(api: PaliaApi, item: Item) -> float:
    """ Cost of item. If it can be gathered or farmed, use sell value, as opportunity cost.
    If it is craftable, check recipe cost. Otherwise, it can only be purchased and use its buy cost. """
    if item.is_source():
        debug(f"{item.name}: source, could be sold for {item.sell_value}")
        return item.sell_value
    elif item.recipe is not None:
        recipe = fetch_recipe(api, item.recipe)
        result = find_recipe_creation_cost(api, recipe)
        debug(f"{item.name}: recipe valued {result}")
        if item.sell_value is not None and item.sell_value > result:
            debug(f"{item.name}: but could be sold for {item.sell_value}")
            result = item.sell_value
        return result
    else:
        debug(f"{item.name}: uncraftable, need to buy for {item.buy_cost}")
        return item.buy_cost
