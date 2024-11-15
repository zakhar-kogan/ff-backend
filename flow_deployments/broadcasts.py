from pathlib import Path

from prefect.client.schemas.schedules import CronSchedule

from src.config import settings
from src.flows.broadcasts.meme import (
    broadcast_next_meme_to_active_1w_ago,
    broadcast_next_meme_to_active_2w_ago,
    broadcast_next_meme_to_active_4w_ago,
    broadcast_next_meme_to_active_15m_ago,
    broadcast_next_meme_to_active_24h_ago,
    broadcast_next_meme_to_active_48h_ago,
)

deployment_broadcast_15m_ago = broadcast_next_meme_to_active_15m_ago.from_source(
    source=str(Path(__file__).parent.parent),
    entrypoint="src/flows/broadcasts/meme.py:broadcast_next_meme_to_active_15m_ago",
).deploy(
    name="broadcast_next_meme_to_active_15m_ago",
    schedules=[CronSchedule(cron="*/15 * * * *", timezone="Europe/London")],
    work_pool_name=settings.ENVIRONMENT,
)

deployment_broadcast_24h_ago = broadcast_next_meme_to_active_24h_ago.from_source(
    source=str(Path(__file__).parent.parent),
    entrypoint="src/flows/broadcasts/meme.py:broadcast_next_meme_to_active_24h_ago",
).deploy(
    name="broadcast_next_meme_to_active_24h_ago",
    schedules=[CronSchedule(cron="5 * * * *", timezone="Europe/London")],
    work_pool_name=settings.ENVIRONMENT,
)

deployment_broadcast_48h_ago = broadcast_next_meme_to_active_48h_ago.from_source(
    source=str(Path(__file__).parent.parent),
    entrypoint="src/flows/broadcasts/meme.py:broadcast_next_meme_to_active_48h_ago",
).deploy(
    name="broadcast_next_meme_to_active_48h_ago",
    schedules=[CronSchedule(cron="5 * * * *", timezone="Europe/London")],
    work_pool_name=settings.ENVIRONMENT,
)

deployment_broadcast_1w_ago = broadcast_next_meme_to_active_1w_ago.from_source(
    source=str(Path(__file__).parent.parent),
    entrypoint="src/flows/broadcasts/meme.py:broadcast_next_meme_to_active_1w_ago",
).deploy(
    name="broadcast_next_meme_to_active_1w_ago",
    schedules=[CronSchedule(cron="7 * * * *", timezone="Europe/London")],
    work_pool_name=settings.ENVIRONMENT,
)

deployment_broadcast_2w_ago = broadcast_next_meme_to_active_2w_ago.from_source(
    source=str(Path(__file__).parent.parent),
    entrypoint="src/flows/broadcasts/meme.py:broadcast_next_meme_to_active_2w_ago",
).deploy(
    name="broadcast_next_meme_to_active_2w_ago",
    schedules=[CronSchedule(cron="8 * * * *", timezone="Europe/London")],
    work_pool_name=settings.ENVIRONMENT,
)

deployment_broadcast_4w_ago = broadcast_next_meme_to_active_4w_ago.from_source(
    source=str(Path(__file__).parent.parent),
    entrypoint="src/flows/broadcasts/meme.py:broadcast_next_meme_to_active_4w_ago",
).deploy(
    name="broadcast_next_meme_to_active_4w_ago",
    schedules=[CronSchedule(cron="9 * * * *", timezone="Europe/London")],
    work_pool_name=settings.ENVIRONMENT,
)
