from tasks.users import create_users
from tasks.posts import create_posts

class SocialNetworkSpider:
    users = []
    posts = []
    likes = []

    def __init__(
            self, *, number_of_users: int, max_post_per_user: int, max_lakes_per_user: int
    ):
        self.max_lakes_per_user = max_lakes_per_user
        self.max_post_per_user = max_post_per_user
        self.number_of_users = number_of_users

    async def create_users(self):
        users_list = await create_users(number_of_users=self.number_of_users)
        self.users = users_list

    async def create_posts(self):
        for user in self.users:
            await create_posts(user=user)