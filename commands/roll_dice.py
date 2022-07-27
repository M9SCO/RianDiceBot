from lib2to3.pgen2.parse import ParseError
from logging import info
from pickle import load

from aiogram.types import Message
from aiogram.utils.exceptions import MessageIsTooLong
from lark import UnexpectedCharacters
from rolling_dice import get_result

from bin._ import PICKLE_SLASH
from bin.bot import dp


@dp.message_handler(regexp=r"(^[\/dkдк])|([dkдк]\d)")
async def roll_dice(message: Message):
    with open(PICKLE_SLASH, 'rb') as f:
        only_slashsed = load(f)
    if message.from_user.id in only_slashsed and not message.is_command():
        return
    text = (message.get_command(True) or message.text).lower().replace(" ", "")

    try:
        result = get_result(text)
        res = f"\n".join(r.total_formula for r in result)
        info(f"{message.from_user.mention} /{text}: {', '.join(str(r.total) for r in result)}")
        return await message.answer(f"{message.from_user.mention} /{text}:\n{res}", parse_mode="HTML")
    except (UnexpectedCharacters, MessageIsTooLong, ParseError):
        pass
