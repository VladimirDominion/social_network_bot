import asyncio
import logging
from typing import List

import aiohttp
from conf import BASE_URL
from faker import Faker
from models import User

fake = Faker()
logger = logging.getLogger(__name__)


def _create_fake_user() -> User:
    user = User(
        email=fake.email(),
        password=fake.password(),
        first_name=fake.first_name(),
        last_name=fake.last_name()
    )
    return user


def _get_fake_user_list(*, number_of_users: int) -> List[User]:
    users_list = []
    for _ in range(number_of_users):
        users_list.append(_create_fake_user())
    return users_list


async def _signup_user(*, user: User, url: str) -> User:
    user_data = user.dict()
    user_data['password_repeat'] = user_data['password']
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=user_data) as resp:
            json_data = await resp.json()
            if resp.status == 201:
                user.id = json_data['id']
                return user
            logging.error(f"Error signup user {resp.status} {json_data}")


async def create_users(*, number_of_users: int) -> List[User]:
    logger.debug("start creation users")
    fake_users_list = _get_fake_user_list(number_of_users=number_of_users)
    created_users_list = []
    logger.debug(fake_users_list)
    url = f'{BASE_URL}/api/users/signup/'
    for task in asyncio.as_completed([_signup_user(user=user, url=url) for user in fake_users_list]):
        created_user = await task
        created_users_list.append(created_user)
    return created_users_list
