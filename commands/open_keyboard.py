from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from bin._ import DICES
from bin.bot import dp



@dp.message_handler(commands=["kb", "keyboard"])
async def open_keyboard(message: Message):
    command, args = message.get_full_command()
    args = args or " /".join(DICES)
    buttons = [KeyboardButton(text="/" + button if not button.startswith("/") else button) for button in
               args.split(" /")]
    rows = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]
    return await message.reply(text=message.html_text,
                               reply_markup=ReplyKeyboardMarkup(rows, resize_keyboard=True, selective=True))
