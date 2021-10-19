from aiounittest import AsyncTestCase, async_test
from parser import parsing
from errors import ParseError


class TesterCalculator(AsyncTestCase):
    "Проверка основной математической логики"
    async def use_formula(self, f: str, expected: int):
        with open("../grammar_calculator.lark") as file:
            self.assertEqual(await parsing(f, file.read()), expected, f"{f}!={expected}")

    @async_test
    async def testing_sum(self):
        "Должно корректно складывать"
        await self.use_formula("1+1", 2)

    @async_test
    async def testing_sub(self):
        "Должно корректно вычитать"
        await self.use_formula("10-1", 9)

    @async_test
    async def testing_mul(self):
        "Должно корректно умножать"

        await self.use_formula("3*3", 9)

    @async_test
    async def testing_dev(self):
        "Должно корректно делить"
        await self.use_formula("10/2", 5)

    @async_test
    async def testing_complex_math_expression(self):
        "парсер должнен уметь обрабатывать комплексные выражения"
        await self.use_formula("((2+2)*2+2+2*2)/2", 7)

    @async_test
    async def testing_wrong_formula(self):
        "парсер должен падать в специальные ошибки, ри непонятной формуле"
        with self.assertRaises(ParseError):
            await self.use_formula("2?2", 0)

class TesterDice(AsyncTestCase):
    # async def roll_dice(self, f: str, max: int):
    #     with open("../grammar_dice.lark") as file:
    #         self.assertTrue(await parsing(f, file.read())<=max, )
    # @async_test
    # async def test_roll(self):
    #     await self.roll_dice("1d20", )
    ...