import logging
import aiohttp
import time

from core.models import User
from core.schemas.user import UserRead, UserRegisteredNotification

log = logging.getLogger(__name__)

WEBHOOK_URL = "https://httpbin.org/post"


async def send_new_user_notification(user: User) -> None:
    wb_data = UserRegisteredNotification(
        user=UserRead.model_validate(user),
        ts=int(time.time()),
    ).model_dump()
    log.info("Notify user created wich data: %s", wb_data)
    async with aiohttp.ClientSession() as session:
        async with session.post(WEBHOOK_URL, json=wb_data) as response:
            data = await response.json()
            log.info("Send webhook, got response: %s", data)
