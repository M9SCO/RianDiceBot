from random import seed
from unittest import TestCase

from src import Dice
from src.exceptions import DiceError


class TesterDice(TestCase):

    def setUp(self) -> None:
        seed(1)

    def test_actual_throw(self):
        """значение Dice.throw сответвует поданному числу"""
        self.assertEqual(Dice(throw=1, face=20).throw, 1)

    def test_actual_face(self):
        """значение Dice.face сответвует поданному числу"""
        self.assertEqual(Dice(throw=1, face=20).face, 20)

    def test_roll_1d20(self):
        """если кидать 1Кчто-то-там, то должно вернуть число"""
        self.assertEqual(Dice(throw=1, face=20).result, [5])

    def test_roll_20d20(self):
        """если кидать много-чего-то-тамКчто-там то должно вернуть лист кубов"""
        expected = [5, 19, 3, 9, 4, 16, 15, 16, 13, 7, 4, 16, 1, 13, 14, 20, 1, 15, 9, 8]
        self.assertEqual(Dice(throw=20, face=20).result, expected)

    def test_roll_3d20l(self):
        """если к кубам добавить сортировку "меньше", то должен поубирать результаты, не проходящие по условию"""
        self.assertEqual(Dice(throw=3, face=20, retain_f=min, retain_n=1).result, [3])

    def test_roll_2d20l3(self):
        """если сортируемое количество превышает количество бросков, то сортировка подавляется"""
        self.assertEqual(Dice(throw=2, face=20, retain_f=min, retain_n=3).result, [5, 19])

    def test_roll_4d20h3(self):
        """если к инициализированным кубам добавить сортировку то должно "урезать" результаты """
        actual = Dice(throw=4, face=20)
        actual.result  # [5, 19, 3, 9]
        actual._retain_f = max
        actual._retain_n = 3
        self.assertEqual(actual.result, [19, 9, 5])

    def test_raise_if_use_part_retain(self):
        """если необходимо урезать количесво бросков, то необходимо подавать retain_f месте с retain_n, а не по одиночке"""
        with self.assertRaises(DiceError):
            self.assertEqual(Dice(throw=1, face=20, retain_f=lambda data: data[0]).result, 5)
