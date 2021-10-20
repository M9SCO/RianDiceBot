from aiounittest import AsyncTestCase, async_test
from src import calculate


class TesterCalculator(AsyncTestCase):
    "Проверка основной математической логики"
    async def use_formula(self, f: str, expected: int):
        self.assertEqual(await calculate(f, "../src/grammar_calculator.lark"), expected, f"{f}!={expected}")

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
        "парсер должен падать в ошибку, при непонятной формуле"
        with self.assertRaises(Exception):
            #ToDo Пофиксить на пробрасывание собственной ошибки
            await self.use_formula("2?2", 0)