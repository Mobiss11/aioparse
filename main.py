import os
import random
import aiohttp
import asyncio
import aiofiles
import json

from aiohttp import ClientConnectorError
from time import perf_counter
from bs4 import BeautifulSoup

from utils.content_gen import StartContent


class AsyncParse:
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    @staticmethod
    def generate_content(link, html_page):
        time_link = perf_counter()
        content = {
            'link': link
        }
        all_img = html_page.body.find_all('img')
        content['imgs'] = [img['src'] for img in all_img if 'src' in img.attrs]

        all_links = html_page.body.find_all('a')
        content['links'] = [link['href'] for link in all_links if 'href' in link.attrs]

        all_scripts = html_page.find_all('script')
        content['scripts'] = str(all_scripts)

        body_content = html_page.find('body')
        content['body_content'] = str(body_content)

        print(f"Затраченное время на ссылку {link}: {(perf_counter() - time_link):.02f}")
        return content

    async def get_content_link(self, link):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(link, headers=self.DEFAULT_HEADERS) as response:
                    content_page = await response.text()
                    soup = BeautifulSoup(content_page, 'html.parser')
                    content = self.generate_content(link, soup)

                    async with aiofiles.open(f'content/{str(random.random())[2:]}.json', 'w') as file:
                        await file.write(json.dumps(content))

            except ClientConnectorError as e:
                print(f"Ошибка подключения: {e}")


def delete_files():
    file_list = os.listdir('content/')
    if file_list:
        for file_name in file_list:
            if file_name.endswith(".json"):
                file_path = os.path.join('content/', file_name)
                os.remove(file_path)


def get_size_content():
    size = 0
    for ele in os.scandir('content/'):
        size += os.path.getsize(ele)

    return size / 1024 / 1024


async def main(links: list) -> None:
    link_tasks = []
    for link in links:
        link_tasks.append(asyncio.create_task(AsyncParse().get_content_link(link)))
    await asyncio.gather(*link_tasks)


if __name__ == '__main__':
    delete_files()
    start_time = perf_counter()
    start_url = 'https://forum.antichat.com/'
    start_content = StartContent().get_links(start_url)

    asyncio.run(main(start_content['links']))
    print('-----------------------------------')
    print('Общее количество ссылок', start_content['count_links'])
    print("Общий объем контента:", get_size_content(), "МБ")
    print(f"Общее затраченное время: {(perf_counter() - start_time):.02f}", 'сек')
