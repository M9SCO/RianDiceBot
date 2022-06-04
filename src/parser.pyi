from lark import Tree

from .modules.Result import Result
from .modules.Dice import Dice


async def simple_calculation(tree: Tree) -> int: ...


async def parse_roll_dice(tree: Tree) -> Dice: ...


async def filtration_dices(tree: Tree) -> Dice: ...


async def get_next_point(tree: Tree) -> int | simple_calculation | parse_roll_dice: ...


async def expect(tree) -> None: ...


async def open_lark(text, path_to_grammar) -> int | simple_calculation | parse_roll_dice: ...

async def get_result(text: str,
                     path_dice_grammar: str = "resources/grammar_dice.lark",
                     path_calc_grammar: str = "resources/grammar_calculator.lark") -> Result: ...
