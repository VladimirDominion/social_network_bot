import asyncio

import pytest

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
        "access": "XXXXXXXXXXXX",
        "refresh": "XXXXXXXXXXXX"
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
def post_results():
    return [
        {'id': 1},
        {'id': 2},
        {'id': 3},
        {'id': 4},
        {'id': 5}
    ]


@pytest.fixture
def fake_post_list(post_results, limit=10, offset=0, count=2, next=None, previous=None):
    return {
        "limit": limit,
        "offset": offset,
        "count": count,
        "next": next,
        "previous": previous,
        "results": post_results
    }
