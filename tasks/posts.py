import logging
import random
from typing import List

import aiohttp
from conf import BASE_URL
from conf import MAX_POST_PER_USER
from faker import Faker
from pydantic import BaseModel
from tasks.auth import get_jwt_headers
from tasks.users import User

fake = Faker()
logger = logging.getLogger(__name__)


class Post(BaseModel):
    id: int = None
    title: str
    text: str
    author: int = None


def _create_fake_post():
    return Post(
        title=fake.name(),
        text=fake.text
    )


def _get_fake_post_list(number_of_posts: int) -> List[User]:
    posts_list = []
    for _ in range(number_of_posts):
        posts_list.append(_create_post())
    return posts_list


async def _create_post(*, post: Post, url: str, session: aiohttp.ClientSession) -> Post:
    with session.post(url, json=post.dict()) as resp:
        if resp.status == 201:
            return await resp.json()
        # TODO handle errors
        logger.error(f"Error creating post {resp.status}")


def _calculate_number_of_posts(*, max_post_per_user: int) -> int:
    assert max_post_per_user > 0, 'MAX_POST_PER_USER should be more then 0'
    return random.randint(1, max_post_per_user) if max_post_per_user > 1 else max_post_per_user


async def create_posts(*, user: User) -> List[Post]:
    url = f'{BASE_URL}/api/posts/'
    count_posts = _calculate_number_of_posts(max_post_per_user=MAX_POST_PER_USER)
    jwt_headers = await get_jwt_headers(user=user)
    posts = []
    fake_posts = _get_fake_post_list(number_of_posts=count_posts)
    async with aiohttp.ClientSession(headers=jwt_headers) as session:
        for task in asyncio.as_completed([_create_post(user=user, url=url) for user in fake_users_list]):
            res = await task
            if res:
                post = Post(id=res['id'], title=res['title'], text=res['text'], author=res['author'])
                posts.append(post)
    return posts


async def get_count_posts(*, user: User) -> int:
    url = f'{BASE_URL}/api/posts/'
    jwt_headers = await get_jwt_headers(user=user)
    async with aiohttp.ClientSession(headers=jwt_headers) as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                json_response = await resp.json()
                return json_response.get('count')
