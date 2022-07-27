from pickle import dump

from bin._ import PICKLE_SLASH
from bin.bot import dp


@dp.errors_handler(exception=FileNotFoundError)
async def add_pickle_file(update, error):
    with open(PICKLE_SLASH, 'wb') as f:
        dump([], f)
    await dp.process_update(update)
    return True