import pytest
import asyncio

from ..tasks.users import _create_fake_user


@pytest.fixture
def fake_user():
    return _create_fake_user()


@pytest.fixture
def number_of_users():
    return 3


@pytest.fixture
def fake_tokens():
    return {
      "access":"XXXXXXXXXXXX",
      "refresh":"XXXXXXXXXXXX"
    }


@pytest.fixture
def fake_jwt_headers():
    return {
        "Authorization": f"Bearer XXXXXXXXXXXX"
    }

@pytest.fixture
def mock_get_jwt_headers(fake_jwt_headers, mocker):
    future = asyncio.Future()
    future.set_result(fake_jwt_headers)
    return future

@pytest.fixture
def mock_get_jwt_token(fake_tokens, mocker):
    future = asyncio.Future()
    future.set_result(fake_tokens)
    return future


@pytest.fixture
def fake_post_list(limit=10, offset=0, count=2, next=None, previous=None, results=[]):
    return {
        "limit": limit,
        "offset": offset,
        "count": count,
        "next": next,
        "previous": previous,
        "results": results
    }