from fastapi import APIRouter

from core.schemas.user import UserRegisteredNotification

router = APIRouter()


@router.post("user-created")
def notify_create_user(info: UserRegisteredNotification):
    """
    This webhook will be triggered when a user is created
    """
