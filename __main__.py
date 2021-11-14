from aiogram import Bot, Dispatcher, executor, types, filters
from lark import UnexpectedCharacters

from src.parser import get_result
from src.exceptions import DiceLimits

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def roller_dice(message: types.Message):

    try:
        result = await get_result(message.text[1:] if message.text.startswith('/') else message.text)
        if isinstance(result, list):
            if len(result) > 10:
                raise DiceLimits

            res = f"\n".join(r.total_formula for r in result)
        else:
            res = result.total_formula
        await message.answer(f"{message.from_user.mention} {message.text}:\n{res}", parse_mode="HTML")
    except (UnexpectedCharacters, DiceLimits):
        pass
executor.start_polling(dp, skip_updates=True)