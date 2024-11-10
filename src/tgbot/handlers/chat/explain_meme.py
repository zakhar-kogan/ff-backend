import base64
import html
import logging

from openai import AsyncOpenAI
from telegram import Message, Update
from telegram.error import Forbidden
from telegram.ext import ContextTypes

from src.config import settings
from src.storage.upload import download_meme_content_from_tg
from src.tgbot.constants import TELEGRAM_CHANNEL_RU_CHAT_ID
from src.tgbot.logs import log
from src.tgbot.service import get_user_by_id
from src.tgbot.utils import check_if_user_chat_member


def encode_image_bytes(image: bytes):
    return base64.b64encode(image).decode("utf-8")


async def call_chatgpt_vision(image: bytes, prompt: str) -> str:
    encoded_image = encode_image_bytes(image)

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    return response.choices[0].message.content


async def explain_meme_ru(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Explain a tg channel post to the user
    Handle message from channel in a chat
    """

    # check that the meme was sent by our bot or the correct user

    our_channel = (
        update.message.sender_chat
        and update.message.sender_chat.id == TELEGRAM_CHANNEL_RU_CHAT_ID
    )
    if our_channel:
        return await generate_and_send_meme_explanation(update.message)

    user_id = update.effective_user.id

    # check that user is in bot
    user_info = await get_user_by_id(user_id)
    active_in_bot = user_info["blocked_bot_at"] is None
    if not active_in_bot:
        # await update.message.set_reaction(reaction=)

        return await update.message.reply_text(
            "🙈 Не вижу тебя в боте. Надо зайти -> @ffmemesbot"
        )

    # check that user subscribed to a channel
    subscribed_to_channel = await check_if_user_chat_member(
        context.bot, user_id, TELEGRAM_CHANNEL_RU_CHAT_ID
    )
    if not subscribed_to_channel:
        return await update.message.reply_text(
            "😵‍💫 Не вижу тебя в канале. Надо подписаться -> @ "
        )

    return await generate_and_send_meme_explanation(update.message)


async def generate_and_send_meme_explanation(message: Message):
    file_id = message.photo[-1].file_id
    image_bytes = await download_meme_content_from_tg(file_id)

    prompt = """
Мама прислала тебе эту смешную картинку. Объясни двумя предложениями, в чем прикол.
Не пересказывай содержание мема и используй неформальную лексику.
    """

    if message.reply_to_message:
        text = message.reply_to_message.text
        if len(text) > 3:
            prompt += (
                f"Эту картинку прислали в ответ на сообщение с таким текстом: '{text}'"
            )

    vision_result = await call_chatgpt_vision(image_bytes, prompt)

    if vision_result:
        vision_result = html.unescape(vision_result)
        try:
            await message.reply_text(vision_result)
        except Forbidden:
            log(
                f"Can't send meme explanation to chat: {vision_result}",
                level=logging.ERROR,
                exc_info=True,
            )


async def explain_meme_en(update: Update, _: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return  # idk why that happens

    file_id = update.message.photo[-1].file_id
    image_bytes = await download_meme_content_from_tg(file_id)
    vision_result = await call_chatgpt_vision(
        image_bytes,
        """
Your mom sent you this funny picture. Explain the joke in two sentences.
Don't retell the meme and use informal language.
        """,
    )

    if vision_result:
        vision_result = html.unescape(vision_result)
        try:
            await update.message.reply_text(vision_result)
        except Forbidden:
            log(
                f"Can't send meme explanation to chat: {vision_result}",
                level=logging.ERROR,
                exc_info=True,
            )
