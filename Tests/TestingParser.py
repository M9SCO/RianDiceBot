from asyncio import run, coroutine

from aiounittest import AsyncTestCase, async_test
from rolling import calculate
from errors import ParseError


class TesterParser(AsyncTestCase):
    async def formula(self, f: str, expected: int):
        self.assertEqual(await calculate(f), expected, f"{f}!={expected}")

    @async_test
    async def testing_sum(self):
        "Должно корректно складывать"
        await self.formula("1+1", 2)

    @async_test
    async def testing_sub(self):
        "Должно корректно вычитать"
        await self.formula("10-1", 9)

    @async_test
    async def testing_mul(self):
        "Должно корректно умножать"

        await self.formula("3*3", 9)

    @async_test
    async def testing_dev(self):
        "Должно корректно делить"
        await self.formula("10/2", 5)

    @async_test
    async def testing_complex_math_expression(self):
        "парсер должнен уметь обрабатывать комплексные выражения"
        await self.formula("((2+2)*2+2+2*2)/2", 7)

    @async_test
    async def testing_wrong_formula(self):
        "парсер должен падать в специальные ошибки, ри непонятной формуле"
        with self.assertRaises(ParseError):
            await self.formula("2?2", 0)

    # def testing_throw_dice(self):
    #     "парсер должен кидать кубы и складывать по математической формуле"
    #     self.assertTrue(parse("1d6+2k6+1д6+1к6") <=30)
