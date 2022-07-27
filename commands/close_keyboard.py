from aiogram.types import Message, ReplyKeyboardRemove

from bin.bot import dp


@dp.message_handler(commands=["h", "hide"])
async def close_keyboard(message: Message):
    return await message.reply(text=message.html_text, reply_markup=ReplyKeyboardRemove())