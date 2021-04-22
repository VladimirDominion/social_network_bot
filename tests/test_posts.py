import aiohttp
import pytest

from tasks.posts import _calculate_number_of_posts, get_count_posts
from .mocks import MockResponse


@pytest.mark.parametrize(
    'max_post_per_user',
    [
        -1,
        0,
        1,
        10
    ]
)
def test_calculate_number_of_posts(max_post_per_user):
    if max_post_per_user < 1:
        with pytest.raises(AssertionError):
            res = _calculate_number_of_posts(max_post_per_user=max_post_per_user)
    elif max_post_per_user == 1:
        res = _calculate_number_of_posts(max_post_per_user=max_post_per_user)
        assert res == 1
    else:
        res = _calculate_number_of_posts(max_post_per_user=max_post_per_user)
        assert 1 <= res <= max_post_per_user


@pytest.mark.asyncio
async def test_get_count_posts(fake_post_list, fake_tokens, mock_get_jwt_headers, fake_user, mocker):
    resp = MockResponse(text="", json=fake_post_list, status=200)
    mocker.patch('aiohttp.ClientSession.get', return_value=resp)
    mocker.patch('tasks.posts.get_jwt_headers', return_value=mock_get_jwt_headers)
    res = await get_count_posts(user=fake_user)
    assert res == 2