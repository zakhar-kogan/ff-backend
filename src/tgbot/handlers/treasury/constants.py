from enum import Enum


class TrxType(str, Enum):
    MEME_UPLOADER = "meme_uploader"
    MEME_UPLOAD_REVIEWER = "meme_upload_reviewer"
    USER_INVITER = "user_inviter"
    USER_INVITER_PREMIUM = "user_inviter_premium"

    MEME_SHARED = "meme_shared"

    UPLOADER_TOP_WEEKLY_1 = "uploader_top_weekly_1"
    UPLOADER_TOP_WEEKLY_2 = "uploader_top_weekly_2"
    UPLOADER_TOP_WEEKLY_3 = "uploader_top_weekly_3"
    UPLOADER_TOP_WEEKLY_4 = "uploader_top_weekly_4"
    UPLOADER_TOP_WEEKLY_5 = "uploader_top_weekly_5"

    DAILY_REWARD = "daily_reward"

    MEME_PUBLISHED = "meme_published"

    SEND = "send"
    RECEIVE = "receive"

    BOOSTER_CHANNEL = "booster_channel"

    PURCHASE_TOKEN = "purchase_token"

    ACTIVE_IN_CHAT = "active_in_chat"
    BOT_REPLY_PAYMENT = "bot_reply_payment"


TREASURY_USER_ID = 1123681771


PAYOUTS = {
    TrxType.MEME_UPLOADER: 5,
    TrxType.USER_INVITER: 100,
    TrxType.USER_INVITER_PREMIUM: 200,
    TrxType.MEME_UPLOAD_REVIEWER: 1,
    TrxType.MEME_SHARED: 10,
    TrxType.UPLOADER_TOP_WEEKLY_1: 500,
    TrxType.UPLOADER_TOP_WEEKLY_2: 300,
    TrxType.UPLOADER_TOP_WEEKLY_3: 200,
    TrxType.UPLOADER_TOP_WEEKLY_4: 100,
    TrxType.UPLOADER_TOP_WEEKLY_5: 50,
    TrxType.DAILY_REWARD: 1,
    TrxType.MEME_PUBLISHED: 50,
    TrxType.BOOSTER_CHANNEL: 500,
    TrxType.ACTIVE_IN_CHAT: 5,
    TrxType.BOT_REPLY_PAYMENT: -1,
}

# TODO: localize
TRX_TYPE_DESCRIPTIONS = {
    TrxType.MEME_UPLOADER: "uploading a meme",
    TrxType.USER_INVITER: "inviting a friend",
    TrxType.USER_INVITER_PREMIUM: "inviting a friend with premium",
    TrxType.MEME_UPLOAD_REVIEWER: "reviewing uploaded meme",
    TrxType.MEME_SHARED: "sharing a meme today",
    TrxType.UPLOADER_TOP_WEEKLY_1: "weekly top 1 meme",
    TrxType.UPLOADER_TOP_WEEKLY_2: "weekly top 2 meme",
    TrxType.UPLOADER_TOP_WEEKLY_3: "weekly top 3 meme",
    TrxType.UPLOADER_TOP_WEEKLY_4: "weekly top 4 meme",
    TrxType.UPLOADER_TOP_WEEKLY_5: "weekly top 5 meme",
    TrxType.DAILY_REWARD: "daily activity",
    TrxType.MEME_PUBLISHED: "meme published in our channel",
    TrxType.BOOSTER_CHANNEL: "boosting the channel",
    TrxType.PURCHASE_TOKEN: "token purchase",
    TrxType.ACTIVE_IN_CHAT: "being active in chat",
    TrxType.BOT_REPLY_PAYMENT: "chatting_with_bot",
}
