from pickle import load, dump

from aiogram.types import Message

from bin._ import PICKLE_SLASH
from bin.bot import dp
from bin.locales import get_locale


@dp.message_handler(commands=["only_slash"])
async def only_slash(message: Message):

    with open(PICKLE_SLASH, 'rb+') as f:
            data = load(f)

    has = False
    if message.from_user.id in data:
        data.remove(message.from_user.id)
    else:
        has = True
        data.append(message.from_user.id)

    with open(PICKLE_SLASH, 'wb') as f:
        dump(data, f)

    await message.answer(text=get_locale(f'ignoring_non_slash_{("off", "on",)[has]}', message.from_user.language_code),
                         parse_mode="HTML")
