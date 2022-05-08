from operator import add, mul, sub, truediv as div
from re import findall, search

from lark import Lark, UnexpectedCharacters

from src.exceptions import ParseError
from src.modules.Result import Result
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


async def open_lark(text, path_to_grammar):
    with open(path_to_grammar, encoding="UTF-8") as f:
        grammar = f.read()
    trees = Lark(grammar, start="start").parse(text)

    return await get_next_point(trees)


async def get_result(text,
                     path_dice_grammar="resources/grammar_dice.lark",
                     path_calc_grammar="resources/grammar_calculator.lark"):
    results = []
    repeats_math = search(r"(^\d+)[хx]|[хx](\d+$)", text)
    repeats = repeats_math.group(1) or repeats_math.group(2) if repeats_math else 1
    for _ in range(int(repeats) if int(repeats) < 10 else 10):
        t = text.replace(repeats_math.group(0), "") if repeats_math else text
        result = Result(raw=t)
        result.dices = []
        for dice in findall(r"(\d*[dkдк]\d+[hlвнd]?\d*)", t):
            value: Dice = await open_lark(text=dice, path_to_grammar=path_dice_grammar)
            result.dices.append((dice, value))
        result.total = await open_lark(text=result.replaced_dices, path_to_grammar=path_calc_grammar)
        if str(result.total) == t:
            raise ParseError
        results.append(result)
    return results
