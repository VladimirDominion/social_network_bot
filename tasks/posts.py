import logging
import random
from typing import List

import aiohttp
from conf import BASE_URL, MAX_POST_PER_USER, MAX_LIKES_PER_USER, POSTS_ON_PAGE
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


def _calculate_random_count_actions(*, max_value: int) -> int:
    assert max_value > 0, 'max_value should be more then 0'
    return random.randint(1, max_value) if max_value > 1 else max_value


async def create_posts(*, user: User) -> List[Post]:
    url = f'{BASE_URL}/api/posts/'
    count_posts = _calculate_random_count_actions(max_value=MAX_POST_PER_USER)
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


async def _get_count_posts(*, user: User) -> int:
    url = f'{BASE_URL}/api/posts/'
    jwt_headers = await get_jwt_headers(user=user)
    async with aiohttp.ClientSession(headers=jwt_headers) as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                json_response = await resp.json()
                return json_response.get('count')

def _select_posts_for_likes(*, number_of_likes: int, count_posts: int) -> List[int]:
    assert (
            isinstance(number_of_likes, int) and isinstance(count_posts, int)
    ), 'number_of_likes and count_posts should be int'
    assert (
        number_of_likes > 0 and count_posts > 0
    ), f'number_of_likes and count_posts should be more then 0 for now {count_posts=} {number_of_likes=}'
    max_val = number_of_likes if number_of_likes <= count_posts else count_posts
    return random.sample(range(count_posts), k=max_val)


class BatchPosts(BaseModel):
    limit: int
    offset: int
    post_numbers: List[int]


def _make_batches_of_posts(*, post_for_likes: List[int], count_posts: int, post_on_page: int) -> List[BatchPosts]:
    assert isinstance(post_for_likes, list), f'post_for_likes should be a list {post_for_likes=}'
    assert len(post_for_likes) > 0, f'post_for_likes is empty {post_for_likes=}'

    assert isinstance(count_posts, int), f'count_posts should be int {count_posts=}'
    assert count_posts > 0, f'count_posts should be more than 0 {count_posts=}'
    pages = (count_posts // post_on_page + 1) or 1
    batch_post_list = []
    post_for_likes.sort()
    for page in range(1, pages + 1):
        start = (page * post_on_page) - post_on_page
        end = (page * post_on_page)
        post_numbers = [n for n in post_for_likes if start <= n <= end]
        if post_numbers:
            batch_post_list.append(BatchPosts(limit=post_on_page, offset=start, post_numbers=post_numbers))
    return batch_post_list


def _get_post_list_url(*, limit: int, offset: int) -> str:
    return f'{BASE_URL}/api/posts/?limit={limit}&offset={offset}'


def _get_post_like_url(*, post_id: int) -> str:
    return f'{BASE_URL}/api/posts/{post_id}/like/'


def _extract_post_urls(*, post_list: List[dict], post_numbers: List[int], posts_on_page: int) -> List[str]:
    url_list = []
    for post_number in post_numbers:
        n = (post_number % posts_on_page) - 1
        if len(post_list) >= n:
            post = post_list[n]
            url = _get_post_like_url(post_id=post['id'])
            url_list.append(url)
    return url_list



async def _get_post_urls(*, session: aiohttp.ClientSession, post_batches: List[BatchPosts]) -> List[str]:
    post_urls = []
    for post_batch in post_batches:
        url = _get_post_list_url(limit=post_batch.limit, offset=post_batch.offset)
        async with session.get(url) as resp:
            if resp.status == 200:
                posts = await resp.json()
                post_urls += _extract_post_urls(post_list=posts['result'], post_numbers=post_batch.post_numbers)
    return post_urls



async def _make_likes_for_user(*, session: aiohttp.ClientSession, post_batches: List[BatchPosts]):
    data = {
        'kind': True
    }
    async with session.post(url, json=data) as resp:
        pass


async def make_likes(user_list: List[User]):
    assert len(user_list) > 0, 'Count users should be more than 0'
    count_posts = _get_count_posts(user_list[0])
    for user in user_list:
        number_of_likes = _calculate_random_count_actions(MAX_LIKES_PER_USER)
        posts_for_likes = _select_posts_for_likes(number_of_likes=number_of_likes, count_posts=count_posts)
        post_batches = _make_batches_of_posts(
            post_for_likes=posts_for_likes, count_posts=count_posts, post_on_page=POSTS_ON_PAGE
        )
        jwt_headers = await get_jwt_headers(user=user)
        async with aiohttp.ClientSession(headers=jwt_headers) as session:
            await _make_likes_for_user(session=session, post_batches=post_batches)




