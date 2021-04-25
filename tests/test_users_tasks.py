import pytest
from models import User

from .mocks import MockResponse
from ..tasks.users import _signup_user, _create_fake_user, _get_fake_user_list, create_users


@pytest.mark.asyncio
async def test_signup_user(fake_user, mocker):
    data = fake_user.dict()
    data['id'] = 1
    resp = MockResponse(text="", json=data, status=201)
    mocker.patch('aiohttp.ClientSession.post', return_value=resp)
    res = await _signup_user(user=fake_user, url='fake_url')
    assert res.email == fake_user.email
    assert res.id == 1


@pytest.mark.asyncio
async def test_create_users(number_of_users, fake_user, mocker):
    data = fake_user.dict()
    data['id'] = 1
    resp = MockResponse(text="", json=data, status=201)
    mocker.patch('aiohttp.ClientSession.post', return_value=resp)
    users = await create_users(number_of_users=number_of_users)
    assert len(users) == number_of_users


def test_create_fake_user():
    res = _create_fake_user()
    assert isinstance(res, User)
    assert '@' in res.email
    assert len(res.first_name) > 0
    assert len(res.last_name) > 0
    assert len(res.password) > 6


@pytest.mark.parametrize(
    "number_of_users",
    [
        1,
        3,
        5,
    ]
)
def test_get_fake_user_list(number_of_users):
    res = _get_fake_user_list(number_of_users=number_of_users)
    assert len(res) == number_of_users
    for user in res:
        assert '@' in user.email

