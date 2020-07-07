import os
import asyncio
from preprocessing.crawling import get_country_list_from_eu4_wiki
from preprocessing.utils import async_requester, image_download

IMG_DIR_PATH = '../static/img/country_flags/'


def main_code():
    if not os.path.isdir(IMG_DIR_PATH):
        raise FileNotFoundError

    country_list = get_country_list_from_eu4_wiki(with_img_url=True)
    task_stack = []
    loop = asyncio.get_event_loop()
    for country in country_list:
        url = country['img_src']
        path = IMG_DIR_PATH + country['img_name']
        task_stack.append(async_requester(loop, image_download, url, path))
    loop.run_until_complete(asyncio.wait(task_stack))
    print('* Task Finished!')


if __name__ == '__main__':
    main_code()
