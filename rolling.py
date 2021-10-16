from operator import add, mul, sub, truediv as div, neg
from random import randint

from lark import Lark, Tree
from lark.exceptions import UnexpectedCharacters

from __config__ import GRAMMAR, MAX_THROWN, MAX_FACES
from errors import NotFoundMethod, ParseError, DiceLimits

__all__ = ["parse"]


def calculation(tree: Tree):
    match tree.data:
        case "add":
            f = add
        case "sub":
            f = sub
        case "mul":
            f = mul
        case "div":
            f = div
        case _ as unknown_method:
            raise NotFoundMethod("Not found method: " + unknown_method)
    return f(*(get_next_point(child) for child in tree.children))


def roll_dice(tree: Tree):
    if len(tree.children) == 2:
        thrown, face = [get_next_point(child) for child in tree.children]
    else:
        thrown, face = 1, get_next_point(tree.children[0])[0]

    if thrown > MAX_THROWN:
        raise DiceLimits("Thrown dices must be interval 0< and >" + str(MAX_THROWN))
    elif face > MAX_FACES:
        raise DiceLimits("Faces dices must be interval 0< and >" + str(MAX_FACES))
    return sum([randint(1, face) for _ in range(thrown)])


def get_next_point(tree: Tree):
    match tree.data:
        case "dice":
            return roll_dice(tree)
        case "add" | "sub" | "mul" | "div":
            return calculation(tree)
        case "to_int":
            return int(tree.children[0])
        case "res":
            return sum(get_next_point(child) for child in tree.children)
        case _ as unknown:
            raise ParseError("Can't parse " + unknown)


def parse(text: str):
    try:
        return get_next_point(Lark(GRAMMAR, start="start").parse(text))
    except UnexpectedCharacters as e:
        raise ParseError(e)
