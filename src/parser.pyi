from lark import Tree

from src.Dice import Dice


async def simple_calculation(tree: Tree) -> int: ...


async def parse_roll_dice(tree: Tree) -> Dice: ...


async def filtration_dices(tree: Tree) -> Dice: ...


async def get_next_point(tree: Tree) -> int | simple_calculation | parse_roll_dice: ...


async def expect(tree) -> None: ...


async def parsing(text: str, grammar: str) -> list[int] | list[list[int]] | int: ...


async def calculate(text: str, path_to_grammar: str = "src/grammar_calculator.lark") -> int: ...


async def roll_dices(text: str, path_to_grammar: str = "src/grammar_dice.lark") -> list[Dice] | Dice: ...


async def get_result(text: str,
                     path_dice_grammar: str = "src/grammar_dice.lark",
                     path_calc_grammar: str = "src/grammar_calculator.lark") -> str: ...
