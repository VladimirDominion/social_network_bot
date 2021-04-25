import asyncio
import logging

from conf import MAX_POST_PER_USER, MAX_LIKES_PER_USER, NUMBER_OF_USERS
from spiders.social_network_spider import SocialNetworkSpider

logging.basicConfig(level=logging.DEBUG)


async def main():
    """ """
    spider = SocialNetworkSpider(
        number_of_users=NUMBER_OF_USERS, max_post_per_user=MAX_POST_PER_USER, max_lakes_per_user=MAX_LIKES_PER_USER
    )
    await spider.run()


if __name__ == '__main__':
    asyncio.run(main())



