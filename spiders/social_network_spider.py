import logging

from tasks.posts import create_posts, create_likes
from tasks.users import create_users

logger = logging.getLogger(__name__)


class SocialNetworkSpider:
    users = []
    likes = []

    def __init__(
            self, *, number_of_users: int, max_post_per_user: int, max_lakes_per_user: int
    ):
        self.max_lakes_per_user = max_lakes_per_user
        self.max_post_per_user = max_post_per_user
        self.number_of_users = number_of_users

    async def make_users(self):
        users_list = await create_users(number_of_users=self.number_of_users)
        self.users = users_list

    async def make_posts(self):
        logger.debug(self.users)
        for user in self.users:
            await create_posts(user=user)

    async def run(self):
        await self.make_users()
        await self.make_posts()
        await create_likes(user_list=self.users)
