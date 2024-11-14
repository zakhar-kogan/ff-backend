import datetime
import re

from telegram import Bot

from src.tgbot.constants import UserType
from src.tgbot.handlers.treasury.constants import TrxType
from src.tgbot.handlers.treasury.payments import pay_if_not_paid_with_alert
from src.tgbot.logs import log
from src.tgbot.senders.invite import send_successfull_invitation_alert
from src.tgbot.service import (
    get_tg_user_by_id,
    get_user_by_id,
    log_user_deep_link,
    update_user,
)

LINK_UNDER_MEME_PATTERN = r"s_\d+_\d+"


async def handle_deep_link_used(
    bot: Bot, invited_user: dict, invited_user_name: str, deep_link: str
):
    """Handle deep link usage, including user invitations."""
    await log_user_deep_link(invited_user["id"], deep_link)

    # IDEA: reward users for deep link usage

    if not re.match(LINK_UNDER_MEME_PATTERN, deep_link):
        return

    _, user_id, _ = deep_link.split("_")
    invitor_user_id = int(user_id)

    if invitor_user_id == invited_user["id"]:
        return  # User clicked their own link

    invitor_user = await get_user_by_id(invitor_user_id)
    if not invitor_user:
        return  # Invitor doesn't exist

    if invited_user.get("inviter_id"):
        # user was already invited
        return

    # Check if user was created in last minute
    created_at = invited_user["created_at"]
    one_minute_ago = str(datetime.datetime.now() - datetime.timedelta(minutes=1))
    await log(f"created_at: {created_at}, one_minute_ago: {one_minute_ago}")
    if created_at < one_minute_ago:
        return

    await update_user(invited_user["id"], inviter_id=invitor_user_id)

    if invitor_user["type"] == UserType.BLOCKED_BOT:
        return await log(
            f"""
❌ {invited_user_name} was invited by #{invitor_user_id}
but his type is {invitor_user["type"]}
        """
        )

    invited_user_tg = await get_tg_user_by_id(invited_user["id"])
    trx_type = (
        TrxType.USER_INVITER_PREMIUM
        if invited_user_tg and invited_user_tg.get("is_premium")
        else TrxType.USER_INVITER
    )

    res = await pay_if_not_paid_with_alert(
        bot,
        invitor_user_id,
        trx_type,
        external_id=str(invited_user["id"]),
    )

    if res:
        await send_successfull_invitation_alert(invitor_user_id, invited_user_name)
        await log(f"🤝 #{invitor_user_id} invited {invited_user_name}")

    else:
        # already rewarded for invitation
        # -- invite for  sharing
        today = datetime.today().date().strftime("%Y-%m-%d")
        res = await pay_if_not_paid_with_alert(
            bot,
            invitor_user_id,
            type=TrxType.MEME_SHARED,
            external_id=today,
        )

        await log(f"💌 #{invitor_user_id} shared meme to {invited_user_name}")
