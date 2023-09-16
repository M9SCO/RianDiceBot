from uuid import uuid4

from PowerfulDiceRoller import get_result
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from lark import UnexpectedCharacters

from bin._ import DICES
from bin.bot import dp, bot


@dp.inline_handler()
async def inline_roll_dice(inline_query: InlineQuery):
    items = []
    if not inline_query.query:
        dices = DICES
    else:
        dices = [inline_query.query]
    for dice in dices:
        try:
            result = get_result(dice)
            total = "\n".join(r.total_formula for r in result)
            result_str = f"{inline_query.from_user.mention} {dice}:\n{total}"
            items.append(InlineQueryResultArticle(id=uuid4().__str__(),
                                                  title=f"Roll: {dice}",
                                                  input_message_content=InputTextMessageContent(result_str,
                                                                                                parse_mode="HTML")))
        except(UnexpectedCharacters):
            pass
    await bot.answer_inline_query(inline_query.id, results=items, cache_time=1)