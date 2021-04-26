import logging

import aiohttp
from conf import BASE_URL
from models import User

logger = logging.getLogger(__name__)


async def get_jwt_token(*, user: User) -> dict:
    """
    :param user:
    :return: dict {'access': 'zzzz', 'refresh': 'xxxx'}
    """
    url = f'{BASE_URL}/api/token/'
    data = {
        'email': user.email,
        'password': user.password
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            response_data = await resp.json()
            if resp.status == 200:
                return response_data
            logger.error(f'{resp.status} {response_data}')

def make_jwt_headers(*, tokens: dict) -> dict:
    return {
        "Authorization": f"Bearer {tokens['access']}"
    }


async def get_jwt_headers(*, user: User) -> dict:
    tokens = await get_jwt_token(user=user)
    return make_jwt_headers(tokens=tokens)
