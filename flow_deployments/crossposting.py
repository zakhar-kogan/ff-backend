from prefect.client.schemas.schedules import CronSchedule

from src.flows.crossposting.meme import (
    post_meme_to_tgchannelen,
    post_meme_to_tgchannelru,
)

deployment_crossposting_tgchannelen = post_meme_to_tgchannelen.serve(
    name="post_meme_to_tgchannelen",
    schedules=[CronSchedule(cron="40 8,10,14,18,20 * * *", timezone="Europe/Moscow")],
)

deployment_crossposting_tgchannelen.apply()


deployment_crossposting_tgchannelru = post_meme_to_tgchannelru.serve(
    name="post_meme_to_tgchannelru",
    schedules=[CronSchedule(cron="20 8,10,12,14 * * *", timezone="Europe/Moscow")],
)

deployment_crossposting_tgchannelru.apply()
