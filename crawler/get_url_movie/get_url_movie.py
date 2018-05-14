
import requests
import sys
import webbrowser
from bs4 import BeautifulSoup
from urllib import parse
from urllib import request


class Crawler(object):

    def __init__(self, start_url):
        self.start_url = start_url
        self.domain = '{uri.scheme}://{uri.netloc}'.format(
            uri=parse.urlparse(self.start_url))

    @staticmethod
    def request(url, **kwargs):
        """
        网络请求,返回response对象
        :return:
        """
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers, **kwargs)
            # status = response.status_code
        except Exception as e:
            print(e)
            sys.exit()
        return response

    @staticmethod
    def get_page(url, code):
        """
        code='GB2312' or 'utf-8'
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        req = request.Request(url=url, headers=headers)
        response = request.urlopen(req, timeout=30)
        page = response.read().decode(code)
        return page

    def parse_brand(self, response):
        raise NotImplementedError

    def parse_body(self, response):
        """
        解析正文,由子类实现
        :param response: 爬虫返回的response对象
        :return: 返回经过处理的html正文文本
        """
        raise NotImplementedError


class Dytt(Crawler):
    """docstring for Dytt"""

    def get_list(self, url, name):
        try:
            response = self.request(url)
            soup = BeautifulSoup(response.content, "html.parser")
            page = soup.find('div', {'class': 'co_content8'})
            for k, l in enumerate(page.find_all('a')):
                if name in l.text:
                    yield k + 1, l.text, self.domain + l['href']
        except Exception as e:
            yield 'Sorry!', 'No result!'


class Meijuba(Crawler):
    """docstring for Dytt"""

    def get_title_list(self, url, name):
        try:
            response = self.request(url)
            soup = BeautifulSoup(response.content, "html.parser")
            page = soup.find('div', {'class': 'box_bg_c'})
            for k, ul in enumerate(page.find_all('ul')):
                a = ul.find_all('li')[0].find('a')
                yield(k + 1, a.text, self.domain + a['href'])
        except Exception as e:
            print(e)
            yield 'Sorry!', 'No result!'

    def get_url_list(self, url):
        try:
            response = self.request(url)
            soup = BeautifulSoup(response.content, "html.parser")
            page = soup.find('ul', {'class': 'downurl down-list'})
            for k, li in enumerate(page.find_all('li')):
                a = li.find('span', {'class': 'down-title'}).find('a')
                yield k + 1, a.text, a['href']
        except Exception as e:
            print(e)
            yield 'Sorry!', 'No result!'


def open_url(titles):
    if len(titles) == 0:
        return False
    print('-' * 50)
    for t in titles:
        print(t)
    print('-' * 50)

    while True:
        choose_title = input('(b == back) Please choose: ')
        if choose_title == 'b':
            return True
        if not choose_title.isdigit():
            print('Just support number! Try again!')
            continue
        num = int(choose_title)
        if num > len(titles) or num <= 0:
            print('Sorry, list index out of range! Try again!')
        else:
            break
    dest_url = titles[num - 1][2]
    webbrowser.open(dest_url)


def main():
    choose_type = input('Choose url (1.电影天堂 2.美剧吧 3.dy2018): ')
    if not choose_type.isdigit():
        print('Just support number!')
        return False
    while True:
        if choose_type == '3':
            webbrowser.open('https://www.dy2018.com/html/gndy/')
            return True
        name = input('Moive name: ')
        if name == '':
            return False
        info = {'1': {'url': 'http://s.ygdy8.com/plus/so.php?{}',
                      'query': {
                          'kwtype': 0,
                          'searchtype': 'title',
                          'keyword': name.encode('gb2312')
                      }},
                '2': {'url': 'http://www.meiju8.cc/search.php?{}',
                      'query': 'kw={}'.format(name)
                      },
                '3': {'url': 'https://www.dy2018.com/html/gndy/',
                      'query': ''
                      }
                }

        start_url = info[choose_type]['url']
        query = info[choose_type]['query']
        titles = []
        if choose_type == '1':
            url = start_url.format(parse.urlencode(query))
            dytt = Dytt(start_url)
            for l in dytt.get_list(url, name):
                titles.append(l)
        elif choose_type == '2':
            url = start_url.format(query)
            meijuba = Meijuba(start_url)
            for title in meijuba.get_title_list(url, name):
                titles.append(title)
            '''
            print('-' * 50)
            for content in meijuba.get_url_list(dest_url):
                print(content)
            print('-' * 50)
            '''
        if not open_url(titles):
            return False


if __name__ == '__main__':
    while True:
        main()
