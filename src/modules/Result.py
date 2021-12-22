from dataclasses import dataclass

from .Dice import Dice


@dataclass
class Result:
    raw: str
    total: int = None
    dices: list[tuple[str, Dice]] = None

    @property
    def total_formula(self):
        result = self.raw
        for dice, cls in self.dices:
            result = result.replace(dice, cls.to_str(view_retains=True, ), 1)
        return result + f"={self.total}"

    @property
    def replaced_dices(self):
        result = self.raw
        for dice, cls in self.dices:
            result = result.replace(dice, str(cls.total), 1)
        return result