from uuid import uuid4

from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from lark import UnexpectedCharacters

from src import get_result
from telegram.bot import dp, bot
from telegram.config import DICES


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
        except(UnexpectedCharacters):
            pass
    await bot.answer_inline_query(inline_query.id, results=items, cache_time=1)