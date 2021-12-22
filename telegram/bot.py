from aiogram import Bot, Dispatcher

from telegram.config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

from .commands import open_keyboard, close_keyboard, roller_dice
from .inline_methods import inline_roll_dice

__all__ = (
    "open_keyboard", "close_keyboard", "roller_dice",

    "inline_roll_dice"
)

