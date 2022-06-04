from asyncio import run
from random import seed
from time import time
from unittest import TestCase

from src.modules.Result import Result
from src import get_result


class TesterGetResult(TestCase):

    def getter(self, formula):
        return run(get_result(formula, "../resources/grammar_dice.lark", "../resources/grammar_calculator.lark"))

    def setUp(self) -> None:
        seed(1)

    def test_get_with_single_dice(self):
        '''Количество кинутых кубов должны совпадать c результирующим списком'''
        self.assertEqual(len(self.getter("d20")[0].dices), 1)

    def test_get_with_calculating(self):
        '''сумма должна считаться точно'''
        self.assertEqual(self.getter("2+2*2")[0].total, 6)

    def test_get_formula(self):
        '''результат кубов должен определяться правильно'''
        self.assertEqual(self.getter("3к6в2+1")[0].total, 8)

    def test_calc_formula(self):
        '''результат кубов должен определяться правильно'''
        self.assertEqual(self.getter("d6+d6+d6+d6")[0].total, 11)

    def test_get_repeat_dices_start(self):
        '''Если используется xN то возвращать должен лист'''
        self.assertEqual(self.getter("6x3к6в2+1")[5].total, 10)

    def test_get_result_formula(self):
        '''Результирующую строчку при отсеивании больших меньших значений должен возвращать корректную'''
        result = self.getter("4к6+1")[0]
        self.assertEqual(result.total, 12)
        self.assertEqual(result.replaced_dices, "11+1")
        self.assertEqual(result.total_formula, "[2+5+1+3]+1=12")

    def test_get_result_formula_with_retains(self):
        '''Результирующую строчку при отсеивании больших меньших значений должен возвращать корректную'''
        result = self.getter("4к1в3+1")[0]
        self.assertEqual(result.total, 4)
        self.assertEqual(result.replaced_dices, "3+1")
        self.assertEqual(result.total_formula, "[1+1+1+<strike>1</strike>]+1=4")

    def test_get_multiline_result_formula(self):
        '''Если используется мультибросок, то должен возвращать список классов Result'''
        self.assertTrue(self.getter("6х4к6в3+1"), list)

    def test_stress(self):
        strated = time()
        self.getter("100000d1000")
        self.assertTrue(time() - strated < 1)