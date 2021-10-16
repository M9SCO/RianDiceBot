from aiounittest import AsyncTestCase
from rolling import parse
from errors import ParseError


class TesterParser(AsyncTestCase):
    def formula(self, f:str, expected: int):
        self.assertEqual(parse(f), expected, f"{f}!={expected}")


    def testing_sum(self):
        "Должно корректно складывать"
        self.formula("1+1", 2)

    def testing_sub(self):
        "Должно корректно вычитать"
        self.formula("10-1", 9)

    def testing_mul(self):
        "Должно корректно умножать"

        self.formula("3*3", 9)

    def testing_dev(self):
        "Должно корректно делить"
        self.formula("10/2", 5)

    def testing_complex_math_expression(self):
        "парсер должнен уметь обрабатывать комплексные выражения"
        self.formula("((2+2)*2+2+2*2)/2", 7)

    def testing_wrong_formula(self):
        "парсер должен падать в специальные ошибки, ри непонятной формуле"
        with self.assertRaises(ParseError):
            self.formula("2?2", 0)

    def testing_throw_dice(self):
        "парсер должен кидать кубы и складывать по математической формуле"
        self.assertTrue(parse("1d6+2k6+1д6+1к6") <=30)

    def testing_throw_dice(self):
        "парсер должен кидать кубы и складывать по математической формуле"
        self.assertTrue(parse("1d6+2k6+1д6+1к6") <= 30)