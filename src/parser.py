from operator import add, mul, sub, truediv as div
from re import findall

from lark import Lark

from exceptions import ParseError
from src.Dice import Dice

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


async def expect(tree):
    match tree.data:
        case "repeat_sw" | "repeat_ew" \
            if "repeat_sw" in (tree.children[0].data, tree.children[1].data) or \
            "reoeat_ew" in  (tree.children[0].data, tree.children[1].data):

            raise ParseError("Illegal use recursion")


async def get_next_point(tree):
    await expect(tree)
    match tree.data:
        case "add" | "sub" | "mul" | "div":
            return await simple_calculation(tree)
        case "to_int":
            return int(tree.children[0])
        case "res":
            return sum([await get_next_point(child) for child in tree.children])
        case "dice":
            return await parse_roll_dice(tree)
        case "repeat_sw":
            result = [await get_next_point(tree.children[1]) for _ in range(await get_next_point(tree.children[0]))]
            if isinstance(result[0], list):
                raise ParseError("Illegal use recursion")
            return result
        case "repeat_ew":
            result = [await get_next_point(tree.children[0]) for _ in range(await get_next_point(tree.children[1]))]
            if isinstance(result[0], list):
                raise ParseError("Illegal use recursion")
            return result
        case "max" | "min":
            result = await filtration_dices(tree)
            return result


async def parsing(text, grammar):
    trees = Lark(grammar, start="start").parse(text, start="start")
    return await get_next_point(trees)


async def calculate(text, path_to_grammar="src/grammar_calculator.lark"):
    with open(path_to_grammar) as f:
        grammar = f.read()

    return await parsing(text, grammar)


async def roll_dices(text, path_to_grammar="src/grammar_dice.lark"):
    with open(path_to_grammar) as f:
        grammar = f.read()
    return await parsing(text, grammar)


async def get_result(text: str):
    formula: str = text
    for dice in findall(r"(\d?[хx]?\d*[dkдк]\d+[hlxвнdх]?\d*)", text):
        formula = formula.replace(dice, str(await roll_dices(dice)))
    print(formula)
    return f"{text}:\n{formula}={await calculate(formula)}"
