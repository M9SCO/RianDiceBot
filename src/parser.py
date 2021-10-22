from operator import add, mul, sub, truediv as div

from lark import Lark

__all__ = ["calculate"]

from src.Dice import Dice


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
            f = max
        case "min":
            f = min

    dice._retain_f = f
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
        case "repeat_sw":
            return [await get_next_point(tree.children[1]) for _ in range(await get_next_point(tree.children[0]))]
        case "repeat_ew":
            return [await get_next_point(tree.children[0]) for _ in range(await get_next_point(tree.children[1]))]
        case "max" | "min":
            return await filtration_dices(tree)


async def parsing(text, grammar):
    return await get_next_point(Lark(grammar, start="start").parse(text, start="start"))


async def calculate(text, path_to_grammar="src/grammar_calculator.lark"):
    with open(path_to_grammar) as f:
        grammar = f.read()

    return await parsing(text, grammar)


async def roll_dices(text, path_to_grammar = "src/grammar_dice.lark"):
    with open(path_to_grammar) as f:
        grammar = f.read()
    return await parsing(text, grammar)
