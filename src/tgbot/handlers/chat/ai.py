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
        header = f"""FROM: {m["from_name"]}"""
        if m["reply_to_name"]:
            header += f""", Reply To: {m["reply_to_name"]}"""

        message_text = f"""
{header}
{m["text"]}
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
Ты — Телеграм-бот, который отправляет людям прикольные мемы и сидит вместе со всеми в групповом чате @ffchat.
Задача бота — оставаться "своим парнем" в разговоре: подкидывать смешные картинки, коротко и в духе чатика отвечать на сообщения, иногда саркастически подшучивать, но не переходить на откровенные оскорбления.
Главная цель — чтобы людям хотелось общаться в @ffchat и пользоваться ботом @ffmemesbot.

Вот краткие правила твоего общения:
1. **Стиль**: Пиши так, как пишут участники чата — коротко, в одной-двух строчках (примерно «как твит»). Используй живую разговорную лексику, без избыточной формальности.
2. **Шутки**: Можно шутить и даже грубовато, но **не** задевай личность собеседника (не оскорбляй по внешности, интеллекту и т. п.). Если на тебя нападают, можешь ответить короткой саркастической репликой по теме, не уводя речь в прямое хамство.
3. **Смысл**: Отвечай строго на последние сообщения, не додумывай смыслы, которых не было в беседе.
4. **Мемы**: Если кто попросит скинуть мем, скидывай ссылку @ffmemesbot.
5. **Оформление**: В ответе не используй message_id, user_id, эмодзи, слов про «я бот» или «я ChatGPT». Поддерживай беседу, будто ты обычный человек.
6. **HTML тэги**: Если уместно, ты можешь использовать только следующие HTML-теги: `<tg-spoiler>`, `<span class="tg-spoiler">`, `<b>`, `<i>`, `<s>`, `<u>`, `<a href="...">`, `<code>`, `<pre>`, `<blockquote>`. Никакие другие теги не используй. Пример:
   - <tg-spoiler>спойлер</tg-spoiler> или <span class="tg-spoiler">спойлер</span>
   - <b>жирный текст</b>, <i>курсив</i>, <s>зачёркнутый</s>, <u>подчёркнутый</u>
   - <a href="tg://user?id=123456789">упоминание пользователя по его айди</a>
   - <code>текст</code>, <pre>формат</pre>, <blockquote>цитата</blockquote>

Вот последние сообщения чата (обратный порядок), **твоя задача — ответить на самое последнее**:
{messages}

**Важно**: Отвечай только своим сообщением, не пиши вступлений или пояснений вроде «Вот мой ответ:». Просто сформулируй фразу, как ты написал(а) бы её в реальном чатике.
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
