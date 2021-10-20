from operator import add, mul, sub, truediv as div
from random import randint

from lark import Lark
from lark.exceptions import UnexpectedCharacters

from exceptions import ParseError

__all__ = ["calculate"]


async def simple_calculation(tree):
    match tree.data:
        case "add":
            f = add
        case "sub":
            f = sub
        case "mul":
            f = mul
        case _:
            f = div
    return f(*[await get_next_point(child) for child in tree.children])


async def roll_dice(tree):
    if len(tree.children) == 2:
        thrown, face = [await get_next_point(child) for child in tree.children]
    else:
        thrown, face = 1, await get_next_point(*tree.children)

    return [randint(1, face) for _ in range(thrown)]


async def get_next_point(tree):
    match tree.data:
        case "add" | "sub" | "mul" | "div":
            return await simple_calculation(tree)
        case "to_int":
            return int(tree.children[0])
        case "res":
            return sum([await get_next_point(child) for child in tree.children])
        case "dice":
            return await roll_dice(tree)


async def parsing(text, grammar):
    try:
        return await get_next_point(Lark(grammar, start="start").parse(text))
    except UnexpectedCharacters as e:
        raise ParseError(e)


async def calculate(text, path_to_grammar="grammar_calculator.lark"):
    with open(path_to_grammar) as f:
        return await parsing(text, f.read())


async def roll_dices(text, path_to_grammar):
    with open(path_to_grammar) as f:
        return await parsing(text, f.read())