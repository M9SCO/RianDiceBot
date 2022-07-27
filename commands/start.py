from aiogram.types import Message, ReplyKeyboardRemove

from bin.bot import dp
from bin.locales import get_locale


@dp.message_handler(commands=["start", "help"])
async def send_hello(message: Message):
    return await message.answer(
        get_locale("help", message.from_user.language_code),
        parse_mode="HTML"
    )