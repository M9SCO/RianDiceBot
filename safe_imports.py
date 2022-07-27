from bin.bot import bot, dp
from bin.locales import get_locale, load_locales
from commands.only_slash import only_slash
from commands.start import send_hello
from inline_requests import roll_dice_query


from commands.open_keyboard import open_keyboard
from commands.close_keyboard import close_keyboard
from commands.roll_dice import roll_dice
from commands.z_stub import add_pickle_file

__all__ = (
    "bot",
    "dp",
    "get_locale",
    "load_locales",
    "open_keyboard",
    "close_keyboard",
    "only_slash",
    "roll_dice",
    "add_pickle_file",
    "roll_dice_query",
    "send_hello"

)


