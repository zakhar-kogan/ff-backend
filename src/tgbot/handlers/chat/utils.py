import asyncio

from telegram import InlineKeyboardMarkup, Message
from telegram.error import BadRequest


async def _reply_and_delete(
    message: Message,
    text: str,
    sleep_sec: int = 5,
    delete_original: bool = True,
    reply_markup: InlineKeyboardMarkup | None = None,
):
    msg = await message.reply_text(
        text,
        reply_markup=reply_markup,
    )
    await asyncio.sleep(sleep_sec)
    await msg.delete()

    if delete_original:
        try:
            await message.delete()
        except BadRequest:
            pass
        return
