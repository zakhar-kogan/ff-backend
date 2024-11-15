from prefect.client.schemas.schedules import CronSchedule
from prefect.deployments import Deployment

from src.config import settings
from src.flows.crossposting.meme import (
    post_meme_to_tgchannelen,
    post_meme_to_tgchannelru,
)

deployment_crossposting_tgchannelen = Deployment.build_from_flow(
    flow=post_meme_to_tgchannelen,
    name="post_meme_to_tgchannelen",
    schedules=[CronSchedule(cron="40 8,10,14,18,20 * * *", timezone="Europe/Moscow")],
    work_pool_name=settings.ENVIRONMENT,
)

deployment_crossposting_tgchannelen.apply()


deployment_crossposting_tgchannelru = Deployment.build_from_flow(
    flow=post_meme_to_tgchannelru,
    name="post_meme_to_tgchannelru",
    schedules=[CronSchedule(cron="20 8,10,12,14 * * *", timezone="Europe/Moscow")],
    work_pool_name=settings.ENVIRONMENT,
)

deployment_crossposting_tgchannelru.apply()
