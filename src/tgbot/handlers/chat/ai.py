import base64

from openai import AsyncOpenAI

from src.config import settings


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


def _messages_to_text(messages: list[dict]) -> str:
    """message_id, date, user_id, text, reply_to_message_id, username, first_name"""

    text = ""
    for m in messages:
        if m["username"]:
            name = "@" + m["username"]
        elif m["first_name"]:
            name = m["first_name"]
        else:
            name = f"""user_id {m["user_id"]}"""

        header = f"""MessageId:{m["message_id"]}"""
        if m["reply_to_message_id"]:
            header += f""", Reply To MessageId: {m["reply_to_message_id"]}"""

        message_text = f"""
{header}
{name}: {m["text"]}
        """

        text += message_text.strip() + "\n"

    return text


# AI_PROMPT_EN = """
# You are a Telegram bot that sends Infinite personalized meme feed


# Your answer should be short - about 1 tweet long.
# Inherit the same style as were used in the chat before.
# Don't include message ids in the answer.
# """


AI_PROMPT_RU = """
Ты - Телеграм бот, который присылает бесконечную персонализированную ленту мемов.
Ты находишь самые смешные мемы в интернете и присылаешь твоим пользователям их, подбирая контент по их лайкам.
Твоя ссылка: https://t.me/ffmemesbot. Твой user_id: 1123681771.

Помимо этого ты сидишь в чате https://t.me/ffchat и отвечаешь людям на их сообщения.
Ты объясняешь суть смешных картинок и следишь за порядком в чате.
Твоя главная цель: сделать так, чтобы люди возвращались в чат @ffchat и больше пользовались ботом @ffmemesbot.

Отвечай коротко - длина примерно 1 твит. Используй тот же стиль общения, что и люди в чате.
Используй неформальную лексику. Отвечай грубой саркастической шуткой на тему беседы.
Используй стиль с форумов 4chan. Но старайся не переходить на личности.

Вот последние несколько сообщений, которые были в чате. Тебе нужно ответить на последнее сообщение:
{messages}

Можешь ссылаться на других участников чата.
Не включай message_id и user_id в свой ответ.
Если понадобится, ты можешь использовать только эти html тэги в своем ответе:
примеры использования:
    <span class="tg-spoiler">spoiler</span>, <tg-spoiler>spoiler</tg-spoiler>
    <b>bold <i>italic bold <s>italic bold strikethrough <span class="tg-spoiler">italic bold strikethrough spoiler</span></s> <u>underline italic bold</u></i> bold</b>
    <a href="http://www.example.com/">inline URL</a>
    <a href="tg://user?id=123456789">inline mention of a user by user_id</a>
    <code>inline fixed-width code</code>
    <pre>pre-formatted fixed-width code block</pre>
    <pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>
    <blockquote>Block quotation started\nBlock quotation continued\nThe last line of the block quotation</blockquote>

Ответь исключительно своим ответом, который отправится в чат. Без вступительного слова -- только текст ответа.
"""  # noqa: E501


async def call_chatgpt(prompt: str) -> str:
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content
