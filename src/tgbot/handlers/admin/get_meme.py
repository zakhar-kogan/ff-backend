"""
    Handle /meme <meme_id> admin/mod command
"""

import asyncio

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ContextTypes,
)

from src.storage.schemas import MemeData
from src.tgbot.constants import UserType
from src.tgbot.senders.meme import send_album_with_memes
from src.tgbot.service import get_meme_by_id, get_user_by_id


async def handle_get_meme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends you the meme by it's id"""
    user = await get_user_by_id(update.effective_user.id)
    if UserType(user["type"]).is_moderator:
        return

    message_split = update.message.text.split()
    if len(message_split) < 2:
        await update.message.reply_text(
            "Please specify a <code>meme_id</code>",
            parse_mode=ParseMode.HTML
        )
        return

    try:
        meme_ids = [int(i) for i in message_split[1:]]
    except ValueError:
        await update.message.reply_text(
            "Please specify a valid <code>meme_id</code> (a number!)",
            parse_mode=ParseMode.HTML
        )
        return

    memes_data = await asyncio.gather(*[get_meme_by_id(meme_id) for meme_id in meme_ids])
    memes = [MemeData(**meme) for meme in memes_data if meme is not None]
    await send_album_with_memes(update.effective_user.id, memes)
