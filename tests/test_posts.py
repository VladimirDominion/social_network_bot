import aiohttp
import pytest
from aiohttp.test_utils import ClientSession

from tasks.posts import (
    _calculate_random_count_actions, _get_count_posts, _select_posts_for_likes, _make_batches_of_posts,
    _extract_post_urls, _get_post_urls
)
from .mocks import MockResponse
from conf import BASE_URL


@pytest.mark.parametrize(
    'max_value',
    [
        -1,
        0,
        1,
        10
    ]
)
def test_calculate_random_count_actions(max_value):
    if max_value < 1:
        with pytest.raises(AssertionError):
            res = _calculate_random_count_actions(max_value=max_value)
    elif max_value == 1:
        res = _calculate_random_count_actions(max_value=max_value)
        assert res == 1
    else:
        res = _calculate_random_count_actions(max_value=max_value)
        assert 1 <= res <= max_value


@pytest.mark.asyncio
async def test_get_count_posts(fake_post_list, fake_tokens, mock_get_jwt_headers, fake_user, mocker):
    resp = MockResponse(text="", json=fake_post_list, status=200)
    mocker.patch('aiohttp.ClientSession.get', return_value=resp)
    mocker.patch('tasks.posts.get_jwt_headers', return_value=mock_get_jwt_headers)
    res = await _get_count_posts(user=fake_user)
    assert res == 2


@pytest.mark.parametrize(
    'number_of_likes, count_posts, expected',
    [
        (3, 10, True),
        (0, 10, False),
        (10, 0, False),
        ('hello', 0, False),
    ]
)
def test_select_posts_for_likes(number_of_likes, count_posts, expected):
    if expected:
        res = _select_posts_for_likes(number_of_likes=number_of_likes, count_posts=count_posts)
        assert isinstance(res, list)
        assert len(res) == number_of_likes
    else:
        with pytest.raises(AssertionError):
            _select_posts_for_likes(number_of_likes=number_of_likes, count_posts=count_posts)


@pytest.mark.parametrize(
    'post_on_page',
    [100]
)
@pytest.mark.parametrize(
    'post_for_likes, count_posts , expected_count, expected_error',
    [
        ([3, 124, 157, 267, 456], 520, 4, False),
        ([3, 4, 7, 12, 14], 520, 1, False),
        ([], 520, 1, True),
        ([3, 4, 7, 12, 14], 0, 1, True)
    ]
)
def test_make_batches_of_posts(post_on_page, post_for_likes, count_posts , expected_count, expected_error):
    # TODO add check data
    if not expected_error:
        res = _make_batches_of_posts(post_for_likes=post_for_likes, count_posts=count_posts, post_on_page=post_on_page)
        assert len(res) == expected_count
    else:
        with pytest.raises(AssertionError):
            _make_batches_of_posts(post_for_likes=post_for_likes, count_posts=count_posts, post_on_page=post_on_page)


@pytest.mark.parametrize(
    'post_numbers, posts_on_page, expected',
    [
        ([1,2], 100, [
            f'{BASE_URL}/api/posts/{1}/like/',
            f'{BASE_URL}/api/posts/{2}/like/',
        ]),
        ([3,1,4], 100, [
            f'{BASE_URL}/api/posts/{3}/like/',
            f'{BASE_URL}/api/posts/{1}/like/',
            f'{BASE_URL}/api/posts/{4}/like/',
        ])
    ]
)
def test_extract_post_urls(post_results, post_numbers, posts_on_page, expected):
    res = _extract_post_urls(post_list=post_results, post_numbers=post_numbers, posts_on_page=posts_on_page)
    assert len(res) == len(post_numbers)
    for url in res:
        assert url in expected


# @pytest.mark.asyncio
# async def test_get_post_urls(fake_post_list, mock_get_jwt_headers, mocker):
#     resp = MockResponse(text="", json=fake_post_list, status=200)
#     mocker.patch('aiohttp.ClientSession.get', return_value=resp)
#     mocker.patch('tasks.posts.get_jwt_headers', return_value=mock_get_jwt_headers)
#     res = _get_post_urls()

