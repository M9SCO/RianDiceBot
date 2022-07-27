from os import environ

from aiogram import Bot, Dispatcher


bot: Bot = Bot(token=environ['TOKEN_TELEGRAM'])
dp: Dispatcher = Dispatcher(bot)



