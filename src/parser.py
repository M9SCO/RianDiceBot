from operator import add, mul, sub, truediv as div
from re import findall, match

from lark import Lark

from src.modules.Dice import Dice

__all__ = ["get_result"]


async def simple_calculation(tree):
    values = [await get_next_point(child) for child in tree.children]
    match tree.data:
        case "add":
            return add(*values)
        case "sub":
            return sub(*values)
        case "mul":
            return mul(*values)
        case "div":
            return div(*values)


async def parse_roll_dice(tree):
    if len(tree.children) == 2:
        thrown, face = [await get_next_point(child) for child in tree.children]
    else:
        thrown, face = 1, await get_next_point(*tree.children)

    return Dice(throw=thrown, face=face)


async def filtration_dices(tree):
    dice: Dice = await get_next_point(tree.children[0])

    match tree.data:
        case "max":
            dice._retain_f = max
        case "min":
            dice._retain_f = min
    dice._retain_n = await get_next_point(tree.children[1]) if len(tree.children) > 1 else 1
    return dice


async def get_next_point(tree):
    match tree.data:
        case "add" | "sub" | "mul" | "div":
            return await simple_calculation(tree)
        case "to_int":
            return int(tree.children[0])
        case "res":
            return sum([await get_next_point(child) for child in tree.children])
        case "dice":
            return await parse_roll_dice(tree)
        case "max" | "min":
            return await filtration_dices(tree)


async def parsing(text, grammar):
    trees = Lark(grammar, start="start").parse(text)
    return await get_next_point(trees)


async def calculate(text, path_to_grammar):
    with open(path_to_grammar, encoding="UTF-8") as f:
        grammar = f.read()

    return await parsing(text, grammar)


async def roll_dices(text, path_to_grammar):
    with open(path_to_grammar, encoding="UTF-8") as f:
        grammar = f.read()
    return await parsing(text, grammar)


async def get_result(text,
                     path_dice_grammar="resources/grammar_dice.lark",
                     path_calc_grammar="resources/grammar_calculator.lark"):
    result = {"total": 0,
              "dices": []}
    formula: str = text
    matching = match(r"^(\d+)[xх]", formula)
    if matching:
        return [await get_result(text.replace(matching.group(0), ""), path_dice_grammar, path_calc_grammar)]
    for dice in findall(r"(\d?[xх]?\d*[dkдк]\d+[hlxхвнd]?\d*)", text):
        value = await roll_dices(text=dice, path_to_grammar=path_dice_grammar)
        result["dices"].append((dice, value))
        formula = formula.replace(dice, str(value), 1)
    result["total"] = await calculate(text=formula, path_to_grammar=path_calc_grammar)
    return result
