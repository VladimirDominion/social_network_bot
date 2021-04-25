import logging

from models import User

from .jwt_auth_mixin import JwtAuthMixin

logger = logging.getLogger(__name__)


class BaseTask(JwtAuthMixin):
    async def get_auth_headers(self, user: User) -> dict:
        return await self.get_jwt_headers(user=user)
