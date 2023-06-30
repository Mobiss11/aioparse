import requests
from bs4 import BeautifulSoup


class StartContent:
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    LINKS_EXCLUDED = [
        'https://www.facebook.com/AntichatCom/',
        'http://vk.com/antichat_com',
        'https://twitter.com/antichatru',
        'https://youtube.com/antichat',
        'https://t.me/antichat',
        'https://passport.webmoney.ru/asp/certview.asp?wmid=867420963014',
        'https://ctf.antichat.com/scoreboard',
        'http://video.antichat.ru',
        'http://antichat.ru/',
        'http://antichat.ru',
        'https://www.hackthebox.eu/home/teams/profile/1417',
        '#'
    ]

    def generate_links(self, start_url, links_body):
        links = []
        for link in links_body:
            if 'href' in link.attrs:
                if link['href'] != start_url and link['href'] not in self.LINKS_EXCLUDED:
                    if link['href'][0] == '/':
                        link['href'] = link['href'][1:]
                    if 'http' in link['href']:
                        links.append(link['href'])
                    else:
                        links.append(start_url + link['href'])

        return links

    def get_links(self, url):
        response = requests.get(url, headers=self.DEFAULT_HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        links_body = soup.find_all('a')
        links = list(set(self.generate_links(url, links_body)))

        start_content = {
            'links': links,
            'count_links': len(links)
        }
        return start_content
