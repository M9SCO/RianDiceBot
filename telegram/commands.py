from logging import info
from pickle import dump, load

from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.exceptions import MessageIsTooLong
from lark import UnexpectedCharacters

from src import get_result
from src.exceptions import ParseError

from .bot import dp
from .config import DICES, ONLY_SLASH_PATH_PICKLE


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


@dp.message_handler(commands=["help", "start"])
async def start(message: Message):
    match message.from_user.language_code:
        case "ru":
            text = """Об этом боте.

Различные варианты использования:
/d100
/20к20
д11
3д4+1
d6+к4
/2к20в - бросить 2 раза двадцатигранник и взять 1 максимальный результат
4d6h3 - бросить 4 шестигранных кубика и оставить только 3 максимальных результата
20к12+3х10 - бросить 20 раз двенадцатигранник, прибавить к результату 3, повторить 10 раз

Как это работает:
{бросков}[dkдк]{граней}, где 
{бросков} - сколько получить случайных результатов;
[dkдк] - один из перечисленных знаков-разделителей;
{граней} - количество граней кидаемого куба.
Для выделения самых [число] больших или меньших результатов броска используйте [hв] [число] или [lн] [чисто] соответственно.
Для повторения нескольких [раз] одинаковых бросков используйте [раз]х[бросок] или [бросок]х[раз]
Бот поддерживает следующие арифметические операции над кубами и числами "+", "-", "*", "/".
А так же расставляет приоритеты в действиях, при использовании круглых и квадратных скобок "(", ")", "[", "]" 
Для того чтобы бот реагировал только на явные команды (начинаются с "/"), используйте команду /only_slash. Повторный её вызов выключит данную опцию

Для открытия клавиатуры часто используемых кубов, нажмите /kb, /keyboard, а для закрытия /hide.
Можно составить свою клавиатуру часто используемых кубов, продолжая команду /kb или /keyboard, разделяя будущие кнопки " /":
/kb /2d20h /d20 /2d20l /d20+1 /d20+2 /d6+к4 - составить клавиатуру из 6 кнопок быстрого набора


Обратная связь - @VilliamFeedbackBot 
"""
        case _:
            text = """About this bot.

Various uses:
/d100
/20k20
d11
3d4+1
d6+k4
/2k20h - roll 2 times and take the highest roll
4d6h3 - roll 4 hexagonal dice and take the 3 highest rolls
20k12+3x10 - roll 20 times, add to result 3, repeat 10 times

How it works:
{throws}[dkdc]{faces}, where 
{throws} - how many random results to get;
[dkdk] - one of the delimiters listed;
{faces} - the number of faces of the dice to throw.
To highlight the [number] larger or smaller roll results, use {roll}[hв]{number} or {roll}[lн]{number} respectively.
To repeat multiple [times] identical rolls, use [times]x[throws] or [throws]x[times]
The bot supports the following arithmetic operations on dice and numbers "+", "-", "*", "/".
Аnd also prioritizes actions, when using round and square brackets "((", ")", "[", "]"" 
If you want to calling the rolling dice bot only "/", use command /only_slash. Calling it again will disable this option

To open the keyboard of the commonly used dice, press /kb, /keyboard, and to close /hide.
You can create your own keyboard for the commonly used dice by continuing the /kb or /keyboard command, separating future buttons " /":
/kb /2d20h /d20 /2d20l /d20+1 /d20+2 /d6+k4 - compose a keyboard with 6 quick dial buttons
  
Feedback - @VilliamFeedbackBot"""
    await message.answer(text, parse_mode="HTML")


@dp.message_handler(commands=["only_slash"])
async def only_slash(message: Message):
    with open(ONLY_SLASH_PATH_PICKLE, 'rb') as f:
        data = load(f)

    has = False
    if message.from_user.id in data:
        data.remove(message.from_user.id)
    else:
        has = True
        data.append(message.from_user.id)

    with open(ONLY_SLASH_PATH_PICKLE, 'wb') as f:
        dump(data, f)

    match message.from_user.language_code:
        case "ru":
            text = f"""Игнорирование "не команда" {"включено" if has else "выключено"}"""
        case _:
            text = f"""Ignoring "not command" has been {"on" if has else "off"}"""
    await message.answer(text, parse_mode="HTML")

@dp.message_handler(regexp=r"(^[\/dkдк])|([dkдк]\d)")
async def roller_dice(message: Message):
    with open(ONLY_SLASH_PATH_PICKLE, 'rb') as f:
        only_slashsed = load(f)
    if message.from_user.id in only_slashsed and not message.is_command():
        return
    text = (message.get_command(True) or message.text).lower().replace(" ", "")

    try:
        result = await get_result(text)
        res = f"\n".join(r.total_formula for r in result)
        info(f"{message.from_user.mention} /{text}: {', '.join(str(r.total) for r in result)}")
        return await message.answer(f"{message.from_user.mention} /{text}:\n{res}", parse_mode="HTML")
    except (UnexpectedCharacters, MessageIsTooLong, ParseError):
        pass
