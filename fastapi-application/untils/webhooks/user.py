import logging
import aiohttp
import time

from core.models import User
from core.schemas.user import UserRead

log = logging.getLogger(__name__)

WEBHOOK_URL = "https://httpbin.org/post"


async def send_new_user_notification(user: User) -> None:
    wb_data = {
        "user": UserRead.model_validate(user).model_dump(),
        "ts": int(time.time()),
    }
    log.info("Notify user created wich data: %s", wb_data)
    async with aiohttp.ClientSession() as session:
        async with session.post(WEBHOOK_URL, json=wb_data) as response:
            data = await response.json()
            log.info("Send webhook, got response: %s", data)
