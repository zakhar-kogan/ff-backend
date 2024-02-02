import httpx
import telegram
from typing import Any
from pydantic import AnyHttpUrl

from src.config import settings
from src.storage.constants import MemeType, MemeStatus
from src.storage.service import update_meme
from src.storage.parsers.constants import USER_AGENT
from src.tgbot.bot import bot


async def download_meme_content_file(
    url: AnyHttpUrl,
) -> bytes | None:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            url,
            headers={"User-Agent": USER_AGENT},
        )
        if response.status_code == 404:
            return None
        
        response.raise_for_status()
        return response.content
    

async def download_meme_content_from_tg(
    file_id: str,
) -> bytes:
    file = await bot.get_file(file_id)
    file_bytearray = await file.download_as_bytearray()
    return bytes(file_bytearray)


async def upload_meme_content_to_tg(
    meme_id: int,
    meme_type: MemeType,
    content: bytes,  # ??
) -> dict[str, Any] | None:
    if meme_type == MemeType.IMAGE:
        try:
            msg = await bot.send_photo(
                chat_id=settings.MEME_STORAGE_TELEGRAM_CHAT_ID, 
                photo=content
            )
        except telegram.error.TimedOut:
            return None

        meme = await update_meme(
            meme_id=meme_id,
            telegram_file_id=msg.photo[-1].file_id,
            # change status to fix possible BROKEN_CONTENT_LINK
            status=MemeStatus.CREATED,  # or add new status "Uploaded?"
        )
    
    if meme_type == MemeType.VIDEO:
        try:
            msg = await bot.send_video(
                chat_id=settings.MEME_STORAGE_TELEGRAM_CHAT_ID, 
                video=content
            )
        except telegram.error.TimedOut:
            return None

        meme = await update_meme(
            meme_id=meme_id,
            telegram_file_id=msg.video.file_id,
        )

    if meme_type == MemeType.ANIMATION:
        try:
            msg = await bot.send_animation(
                chat_id=settings.MEME_STORAGE_TELEGRAM_CHAT_ID, 
                animation=content
            )
        except telegram.error.TimedOut:
            return None

        meme = await update_meme(
            meme_id=meme_id,
            telegram_file_id=msg.animation.file_id,
        )

    return meme