import pytest

from .mocks import MockResponse

from ..tasks.auth import get_jwt_token, get_jwt_headers, make_jwt_headers


@pytest.mark.asyncio
async def test_get_jwt_headers(fake_tokens, fake_user, mocker):
    resp = MockResponse(text="", json=fake_tokens, status=200)
    mocker.patch('aiohttp.ClientSession.post', return_value=resp)
    res = await get_jwt_headers(user=fake_user)
    assert res['Authorization'] == f"Bearer {fake_tokens['access']}"


@pytest.mark.asyncio
async def test_get_jwt_token(fake_tokens, fake_user, mocker):
    resp = MockResponse(text="", json=fake_tokens, status=200)
    mocker.patch('aiohttp.ClientSession.post', return_value=resp)
    res = await get_jwt_token(user=fake_user)
    assert res == fake_tokens
