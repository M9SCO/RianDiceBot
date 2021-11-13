from asyncio import run
from random import seed
from unittest import TestCase

from src import get_result


class TesterGetResult(TestCase):

    def getter(self, formula):
        return run(get_result(formula, "../resources/grammar_dice.lark", "../resources/grammar_calculator.lark"))

    def setUp(self) -> None:
        seed(1)

    def test_get_with_single_dice(self):
        '''Количество кинутых кубов должны совпадать c результирующим списком'''
        self.assertEqual(len(self.getter("d20")["dices"]), 1)

    def test_get_with_calculating(self):
        '''сумма должна считаться точно'''
        self.assertEqual(self.getter("2+2*2"), {'dices': [], 'total': 6})

    def test_get_formula(self):
        '''результат кубов должен определяться правильно'''
        self.assertEqual(self.getter("3к6в2+1")["total"], 8)

    def test_calc_formula(self):
        '''результат кубов должен определяться правильно'''
        self.assertEqual(self.getter("d6+d6+d6+d6")["total"], 11)

    def test_get_repeat_dices_start(self):
        '''Если используется xN то возвращать должен лист'''
        self.assertEqual(self.getter("6x3к6в2+1")[0]["total"], 8)
