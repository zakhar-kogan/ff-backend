import asyncio
import random

from telegram import Update
from telegram.ext import ContextTypes

reactions = ["👍", "😂", "😮", "😢", "😡", "🎉", "👏", "❤️", "🔥"]


async def give_random_reaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Explain a tg channel post to the user
    Handle message from channel in a chat
    """
    await asyncio.sleep(random.random() * 5)

    reaction = random.choice(reactions)
    await update.message.set_reaction(reaction=reaction)
