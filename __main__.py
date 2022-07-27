from logging import basicConfig, INFO

from aiogram.utils import executor

from safe_imports import dp

basicConfig(format='[%(levelname)-8s] %(message)s', level=INFO)

executor.start_polling(dp, skip_updates=True)
