from sys import prefix

from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import HTTPBearer

from core.config import settings

from .auth import router as auth_router
from .users import router as users_router
from .messages import router as messages_router
from .dependencies_examples import router as router_deps_examples

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(prefix=settings.api.v1.prefix, dependencies=[Depends(http_bearer)])
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(messages_router)

router.include_router(
    router_deps_examples,
    prefix=settings.api.v1.deps,
)
