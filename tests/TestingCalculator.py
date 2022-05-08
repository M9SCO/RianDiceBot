from asyncio import run
from unittest import TestCase

from src import open_lark


class TesterCalculator(TestCase):
    "Проверка основной математической логики"

    def use_formula(self, f: str, expected: int):
        self.assertEqual(run(open_lark(f, "../resources/grammar_calculator.lark")), expected, f"{f}!={expected}")

    def testing_sum(self):
        "Должно корректно складывать"
        self.use_formula("1+1", 2)

    def testing_sub(self):
        "Должно корректно вычитать"
        self.use_formula("10-1", 9)

    def testing_mul(self):
        "Должно корректно умножать"

        self.use_formula("3*3", 9)

    def testing_dev(self):
        "Должно корректно делить"
        self.use_formula("10/2", 5)

    def testing_complex_math_expression(self):
        "парсер должнен уметь обрабатывать комплексные выражения"
        self.use_formula("((2+2)*2+2+2*2)/2", 7)

    def testing_wrong_formula(self):
        "парсер должен падать в ошибку, при непонятной формуле"
        with self.assertRaises(Exception):
            # ToDo Пофиксить на пробрасывание собственной ошибки
            self.use_formula("2?2", 0)
