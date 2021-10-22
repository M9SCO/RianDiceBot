from lark.exceptions import UnexpectedCharacters


class DiceError(Exception):
    ...


class ParseError(Exception):
    ...


class NotFoundMethod(DiceError):
    ...


class DiceLimits(DiceError):
    ...
