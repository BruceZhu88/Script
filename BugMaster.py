# coding=utf-8
from __future__ import unicode_literals

import logging
import os
import re
import time

try:
    from urllib.parse import urlparse  # py3
except:
    from urlparse import urlparse  # py2

import pdfkit
import requests
from bs4 import BeautifulSoup

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""


class Crawler(object):
    """
    爬虫基类，所有爬虫都应该继承此类
    """
    name = None

    def __init__(self, name, start_url, num):
        """
        初始化
        :param name: 将要被保存为PDF的文件名称
        :param start_url: 爬虫入口URL
        """
        self.name = name
        self.start_url = start_url
        self.num = num
        self.domain = '{uri.scheme}://{uri.netloc}'.format(
            uri=urlparse(self.start_url))

    @staticmethod
    def request(url, **kwargs):
        """
        网络请求,返回response对象
        :return:
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        response = requests.get(url, headers=headers, **kwargs)
        print(response)
        return response

    def parse_menu(self, response):
        """
        从response中解析出所有目录的URL链接
        """
        raise NotImplementedError

    def parse_body(self, response):
        """
        解析正文,由子类实现
        :param response: 爬虫返回的response对象
        :return: 返回经过处理的html正文文本
        """
        raise NotImplementedError

    def run(self):
        start = time.time()
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
        htmls = []
        n = 0
        while n <= self.num:
            n = n + 1
            print("Page {}".format(n))
            page_url = re.sub("page=\d+", "page={}".format(n), self.start_url)
            for index, url in enumerate( self.parse_menu(self.request(page_url, timeout=60)) ):
                html = self.parse_body(self.request(url))
                f_name = ".".join([str(index), "html"])
                with open(f_name, 'wb') as f:
                    f.write(html)
                htmls.append(f_name)
                time.sleep(2)

        # pdfkit.from_file(htmls, self.name + ".pdf", options=options)
        '''
        for html in htmls:
            os.remove(html)
        '''
        total_time = time.time() - start
        print(u"总共耗时：%f 秒" % total_time)


class BugMasterPythonCrawler(Crawler):
    """
    虫师
    """

    def parse_menu(self, response):
        """
        解析目录结构,获取所有URL目录列表
        :param response 爬虫返回的response对象
        :return: url生成器
        """
        soup = BeautifulSoup(response.content, "html.parser")
        menu_tag = soup.find_all(class_="post post-list-item")
        for m in menu_tag:
            url = m.find("h2").find("a").get("href")
            if not url.startswith("http"):
                url = "".join([self.domain, url])
            yield url

    def parse_body(self, response):
        """
        解析正文
        :param response: 爬虫返回的response对象
        :return: 返回处理后的html文本
        """
        html = ""
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            body = soup.find_all(id="post_detail")[0]

            # 加入标题, 居中显示
            title = soup.find('h2').get_text()
            center_tag = soup.new_tag("center")
            title_tag = soup.new_tag('h1')
            title_tag.string = title
            center_tag.insert(1, title_tag)
            body.insert(1, center_tag)
            html = str(body)
            html = html_template.format(content=html)
            html = html.encode("utf-8")
        except Exception as e:
            # logging.error("解析错误", exc_info=True)
            logging.debug(e)
        return html


if __name__ == '__main__':
    start_url = "http://www.cnblogs.com/fnng/default.aspx?page=1"
    num = 20
    crawler = BugMasterPythonCrawler("虫师", start_url, num)
    crawler.run()
