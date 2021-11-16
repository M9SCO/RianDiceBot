from hashlib import md5
from uuid import uuid4

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineQuery, \
    InlineQueryResultArticle, InputTextMessageContent
from lark import UnexpectedCharacters

from src.exceptions import DiceLimits
from src.parser import get_result

API_TOKEN = '1051818089:AAE5SOq2e0MMLzYOXAEOEl_-GqIMNWXkCu0'
# API_TOKEN = '1626594204:AAF8R-26pfjl5cjp21Oa7mgfdASZGumHycQ'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
DICES = "2d20l", "1d20", "2d20h", "d4", "d6", "d8", "d10", "d12", "d100"


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
            if len(result) > 10:
                raise DiceLimits

            res = f"\n".join(r.total_formula for r in result)
        else:
            res = result.total_formula
        return await message.answer(f"{message.from_user.mention} {message.text}:\n{res}", parse_mode="HTML")
    except (UnexpectedCharacters, DiceLimits):
        pass


@dp.inline_handler()
async def inline_roll_dice(inline_query: InlineQuery):
    items = []
    if not inline_query.query:
        dices = DICES
    else:
        dices = [inline_query.query]
    for dice in dices:
        try:
            result = await get_result(dice)
            if isinstance(result, list):
                total = "\n".join(r.total_formula for r in result)
            else:
                total = result.total_formula
            result_str = f"{inline_query.from_user.mention} {dice}:\n{total}"
            items.append(InlineQueryResultArticle(id=uuid4().__str__(),
                                                  title=f"Roll: {dice}",
                                                  input_message_content=InputTextMessageContent(result_str,
                                                                                                parse_mode="HTML")))
        except(UnexpectedCharacters, DiceLimits):
            pass
    await bot.answer_inline_query(inline_query.id, results=items, cache_time=1)


executor.start_polling(dp, skip_updates=True)
