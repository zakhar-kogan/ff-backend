import asyncio

from telegram import Message, Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from src.tgbot.constants import UserType
from src.tgbot.handlers.treasury.service import get_user_balance, transfer_tokens
from src.tgbot.service import get_user_by_id


async def _reply_and_delete(message: Message, text: str, sleep_sec: int = 5):
    msg = await message.reply_text(text)
    await asyncio.sleep(sleep_sec)
    await msg.delete()
    try:
        await message.delete()
    except BadRequest:
        pass
    return


async def send_tokens_to_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Explain a tg channel post to the user
    Handle message from channel in a chat
    """
    if (
        not update.message
        or not update.message.text
        or not update.message.reply_to_message
    ):
        return

    if not update.message.text[1:].isdigit():
        return await _reply_and_delete(
            update.message,
            "Нужно указать число после плюсика)",
        )

    to_send = int(update.message.text[1:])

    user_id = update.effective_user.id
    balance = await get_user_balance(user_id)

    if balance < to_send:
        return await _reply_and_delete(
            update.message,
            "У тебя нет столько бургеров.....",
        )

    to_user_tg = update.message.reply_to_message.from_user
    if to_user_tg.is_bot:
        return await _reply_and_delete(
            update.message,
            "Мне не нужны твои бургеры, я и есть бургер",
        )

    to_user_id = to_user_tg.id
    if user_id == to_user_id:
        return  # no need to send tokens to yourself

    to_user = await get_user_by_id(to_user_id)
    if not to_user or to_user["type"] == UserType.BLOCKED_BOT:
        return await _reply_and_delete(
            update.message,
            f"Не вижу {to_user_tg.name} в боте! ай-яй-яй 😿",
            sleep_sec=10,
        )

    # add a treasury transaction: -send, +send
    # send a private messages to both users

    await transfer_tokens(user_id, to_user_id, to_send)

    from_user_balance = await get_user_balance(user_id)
    to_user_balance = await get_user_balance(to_user_id)

    await context.bot.send_message(
        chat_id=user_id,
        text=f"""
Бургеры улетели: -{to_send} 🍔

Твой новый баланс: {from_user_balance} 🍔
        """,
    )

    await context.bot.send_message(
        chat_id=to_user_id,
        text=f"""
Вам прислали бургеры: +{to_send} 🍔

Новый баланс {to_user_balance} 🍔
        """,
    )

    # update balances

    await update.message.set_reaction(reaction="👌", is_big=True)
