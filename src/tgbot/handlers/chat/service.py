from sqlalchemy.dialects.postgresql import insert
from telegram import Message

from src.database import (
    execute,
    fetch_one,
    message_tg,
)


async def save_telegram_message(msg: Message) -> None:
    query = (
        insert(message_tg).values(
            message_id=msg.message_id,
            date=msg.date.replace(
                tzinfo=None
            ),  # Remove timezone info to match DB column type
            chat_id=msg.chat.id,
            user_id=msg.from_user.id,
            text=msg.text or msg.caption,
            reply_to_message_id=msg.reply_to_message.message_id
            if msg.reply_to_message
            else None,
        )
        # .returning(message_tg)
    )
    return await execute(query)
