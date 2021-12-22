from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.exceptions import MessageIsTooLong
from lark import UnexpectedCharacters

from src import get_result

from .bot import dp
from .config import DICES


@dp.message_handler(commands=["kb", "keyboard"])
async def open_keyboard(message: Message):
    command, args = message.get_full_command()
    args = args or " /".join(DICES)
    buttons = [KeyboardButton(text="/" + button if not button.startswith("/") else button) for button in
               args.split(" /")]
    rows = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]
    return await message.reply(text=message.html_text,
                               reply_markup=ReplyKeyboardMarkup(rows, resize_keyboard=True, selective=True))


@dp.message_handler(commands=["h", "hide"])
async def close_keyboard(message: Message):
    return await message.reply(text=message.html_text, reply_markup=ReplyKeyboardRemove())


@dp.message_handler()
async def roller_dice(message: Message):
    try:
        result = await get_result(message.text[1:] if message.text.startswith('/') else message.text)
        if isinstance(result, list):
            res = f"\n".join(r.total_formula for r in result)
        else:
            res = result.total_formula
        return await message.answer(f"{message.from_user.mention} {message.text}:\n{res}", parse_mode="HTML")
    except (UnexpectedCharacters, MessageIsTooLong):
        pass
