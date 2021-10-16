class DiceError(Exception):
    ...


class ParseError(DiceError):
    ...


class NotFoundMethod(DiceError):
    ...


class DiceLimits(DiceError):
    ...
