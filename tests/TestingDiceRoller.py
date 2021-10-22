from asyncio import run
from random import seed
from unittest import TestCase

from exceptions import ParseError
from src import roll_dices, Dice


class TesterDice(TestCase):
    def roll_dice(self, f: str) -> Dice | list[Dice]:
        return run(roll_dices(f, "../src/grammar_dice.lark"))

    def setUp(self) -> None:
        seed(1)

    def test_roll_d20(self):
        "Должен кидать одинарный куб даже если это не указано явно"
        self.assertEqual(self.roll_dice("d20", ).result, 5)

    def test_roll_3d6(self):
        """Должен обрабатывать простую нотацию кубов"""
        self.assertEqual(self.roll_dice("3d6", ).result, [2, 5, 1])

    def test_multiply_roll_startswith_x(self):
        """Должен уметь кидать несколько раз подряд кубы если Х указан слева"""
        self.assertEqual([[dice.result] for dice in self.roll_dice("2xd20")], [[5], [19]])

    def test_multiply_roll_endswith_x(self):
        """Должен уметь кидать несколько раз подряд кубы если Х указан справа"""
        self.assertEqual([[dice.result] for dice in self.roll_dice("d20x2")], [[5], [19]])

    def testing_filtration_high_2d20h(self):
        """Должен выбирать максимальный результат, даже если это не указано явно"""
        self.assertEqual(self.roll_dice("2d20h").result, 19)

    def testing_filtration_high_3d6h2(self):
        """Должен выбирать N максимальных кубов"""
        self.assertEqual(self.roll_dice("3d6h2").result, [5, 2])

    def testing_filtration_high_2d20l(self):
        """Должен выбирать минимальный результат, даже если это не указано явно"""
        self.assertEqual(self.roll_dice("2d20l").result, 5)

    def testing_filtration_high_3d6l2(self):
        """Должен выбирать N миниматьных кубов"""
        self.assertEqual(self.roll_dice("3d6l2").result, [1, 2])

    def testing_filtration_high_3d6l4(self):
        """Должен оставить все кубы, если их количество меньше чем необходимо оставить"""
        self.assertEqual(self.roll_dice("3d6l4").result, [2, 5, 1])

    def testing_banchmarc(self):
        """Должен оставить все кубы, если их количество меньше чем необходимо оставить"""
        self.assertIsNotNone(self.roll_dice("10000d100000").result)


    def test_multiply_roll_start_endswith_x(self):
        """должен спотыкаться, если используется формат Nx{dice}xN"""
        with self.assertRaises(ParseError) as e :
            self.roll_dice("2xd20x2")

    def test_multiply_roll_start_startswith_x(self):
        """должен спотыкаться, если используется формат NxNx{dice}"""
        with self.assertRaises(ParseError) as e :
            self.roll_dice("2x2xd20")

