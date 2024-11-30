from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message, Update
from telegram.ext import ContextTypes

from src.tgbot.constants import TELEGRAM_CHANNEL_RU_CHAT_ID, TELEGRAM_CHAT_RU_CHAT_ID
from src.tgbot.handlers.chat.service import save_telegram_message
from src.tgbot.handlers.chat.utils import _reply_and_delete
from src.tgbot.handlers.treasury.service import get_user_balance

AI_REPLY_PRICE = 1  # 🍔


def if_bot_was_mentioned(msg: Message) -> bool:
    print(msg.to_json())
    if msg.text and "@ffmemesbot" in msg.text.lower():
        return True

    if msg.reply_to_message and msg.reply_to_message.from_user:
        user_id = msg.reply_to_message.from_user.id
        if user_id in (
            1123681771,
            TELEGRAM_CHANNEL_RU_CHAT_ID,
            TELEGRAM_CHAT_RU_CHAT_ID,
        ):
            return True

    return False


async def handle_chat_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    await save_telegram_message(msg)

    # Check if message is a reply to bot's message
    # if if_bot_was_mentioned(msg):
    #     await generate_ai_reply_to_a_message(update, context)
    #     return


async def generate_ai_reply_to_a_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id

    # check balance
    balance = await get_user_balance(user_id)
    if balance < AI_REPLY_PRICE:
        text = "Я отвечаю только за бургеры, а у тебя их больше нет!"
        return await _reply_and_delete(
            update.message,
            text,
            sleep_sec=10,
            delete_original=False,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Получить 🍔🍔🍔",
                            url="https://t.me/ffmemesbot?start=kitchen",
                        )
                    ]
                ]
            ),
        )
