import asyncio

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from src.tgbot.handlers.treasury.service import get_user_balance


async def send_tokens_to_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Explain a tg channel post to the user
    Handle message from channel in a chat
    """
    if not update.message or not update.message.text:
        return

    if not update.message.text.isdigit():
        msg = await update.message.reply_text("Нужно указать число)")
        await asyncio.sleep(5)
        await msg.delete()
        try:
            await update.message.delete()
        except BadRequest:
            pass
        return

    to_send = int(update.message.text)

    user_id = update.effective_user.id
    balance = await get_user_balance(user_id)

    if balance < to_send:
        msg = await update.message.reply_text("У тебя нет столько бургиров.....")
        await asyncio.sleep(5)
        await msg.delete()
        try:
            await update.message.delete()
        except BadRequest:
            pass
        return

    # add a treasury transaction: -send, +send
    # send a private messages to both users

    await update.message.reply_text("Пока не доделал, сории")
    await update.message.set_reaction(reaction="👌", is_big=True)
