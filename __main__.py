from aiogram.utils import executor

from telegram.bot import dp


executor.start_polling(dp, skip_updates=True)
