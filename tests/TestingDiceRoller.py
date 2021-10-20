from asyncio import run
from random import seed
from unittest import TestCase

from src import roll_dices


class TesterDice(TestCase):
    def roll_dice(self, f: str):
        return run(roll_dices(f, "../src/grammar_dice.lark"))

    def setUp(self) -> None:
        seed(1)

    def test_roll_d20(self):
        "Должен кидать одинарный куб даже если это не указано явно"
        self.assertListEqual(self.roll_dice("d20", ), [5])

    def test_roll_3d6(self):
        """Должен обрабатывать простую натацию кубов"""
        self.assertListEqual(self.roll_dice("3d6", ), [2, 5, 1])

    def test_multiply_roll_startswith_x(self):
        """Должен уметь кидать несколько раз подряд кубы если Х указан слева"""
        self.assertListEqual(self.roll_dice("2xd20"), [[5], [19]])

    def test_multiply_roll_endswith_x(self):
        """Должен уметь кидать несколько раз подряд кубы если Х указан справа"""
        self.assertListEqual(self.roll_dice("d20x2"), [[5], [19]])

    def test_multiply_roll_start_endswith_x(self):
        """Не должен спотыкаться, если используется формат Nx{dice}xN"""
        self.assertListEqual(self.roll_dice("2xd20x2"), [[[5], [19]], [[3], [9]]])

    def test_multiply_roll_start_startswith_x(self):
        """Не должен спотыкаться, если используется формат NxNx{dice}"""
        self.assertListEqual(self.roll_dice("2x2xd20"), [[[5], [19]], [[3], [9]]])

    def testing_filtration_high_2d20h(self):
        """Должен выбирать максимальный результат, даже если это не указано явно"""
        self.assertListEqual(self.roll_dice("2d20h"), [19])

    def testing_filtration_high_3d6h2(self):
        """Должен выбирать N максимальных кубов"""
        self.assertListEqual(self.roll_dice("3d6h2"), [5, 2])

    def testing_filtration_high_2d20l(self):
        """Должен выбирать минимальный результат, даже если это не указано явно"""
        self.assertListEqual(self.roll_dice("2d20l"), [5])

    def testing_filtration_high_3d6l2(self):
        """Должен выбирать N миниматьных кубов"""
        self.assertListEqual(self.roll_dice("3d6l2"), [1, 2])

    def testing_filtration_high_3d6l4(self):
        """Должен оставить все кубы, если их количество меньше чем необходимо оставить"""
        self.assertListEqual(self.roll_dice("3d6l4"), [1, 2, 5])

