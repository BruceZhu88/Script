# coding=utf-8
from __future__ import unicode_literals

import os
import sqlite3
try:
    from urllib.parse import urlparse  # py3
except:
    from urlparse import urlparse  # py2

import requests
from bs4 import BeautifulSoup


class Crawler(object):
    """
    爬虫基类，所有爬虫都应该继承此类
    """
    name = None

    def __init__(self, db_path, start_url):
        self.db_path = db_path
        self.start_url = start_url
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
        # print(response)
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
        # start = time.time()
        self.parse_body(self.request(self.start_url))
        # pdfkit.from_file(htmls, self.name + ".pdf", options=options)
        # total_time = time.time() - start
        # print(u"总共耗时：%f 秒" % total_time)


class FindDevices(Crawler):

    def parse_body(self, response):
        title = ['name', 'sn', 'p', 't']
        soup = BeautifulSoup(response.content, "html.parser")
        menu_tag = soup.find_all(class_="table table-striped")[0]
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        for k, v in enumerate(menu_tag.find_all("tr")):
            if len(v.find_all('td')) > 0:
                name = '"{}"'.format(v.find_all('td')[0].get_text())
                sn = '"{}"'.format(v.find_all('td')[1].get_text())
                p = '"{}"'.format(v.find_all('td')[2].get_text())
                t = '"{}"'.format(v.find_all('td')[3].get_text())
                k = ','.join(title)
                data = ','.join([name, sn, p, t])
                sql = "INSERT INTO DEVICES ({}) VALUES ({})".format(k, data)
                c.execute(sql)
        conn.commit()
        conn.close()

    @staticmethod
    def SQL(db_path, sql):
        conn = sqlite3.connect(db_path)
        conn.text_factory = str
        value = []
        c = conn.cursor()
        cursor = c.execute(sql)
        if ("select" or "SELECT") not in sql:
            conn.commit()
            conn.close()
        else:
            for row in cursor:
                value.append(row)
        conn.close()
        return value


if __name__ == '__main__':
    while True:
        search = input('Please input your device: ')
        db_path = '{}/devices.db'.format(os.getcwd())
        if os.path.exists(db_path):
            os.remove(db_path)
        create_table = '''CREATE TABLE DEVICES
                            (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
                            NAME           TEXT    NOT NULL,
                            SN               TEXT    NOT NULL,
                            P                TEXT    NOT NULL,
                            T                TEXT    NOT NULL);'''

        start_url = "http://sw.tymphany.com/ptsys/testdevices.php"
        crawler = FindDevices(db_path, start_url)
        crawler.SQL(db_path, create_table)
        try:
            crawler.run()
            sql = 'select * from devices where name like "%{}%"'.format(search)
            results = crawler.SQL(db_path, sql)
            if len(results) > 0:
                t = ['Device', 'SN', 'Person', 'Time']
                print(t[0].ljust(25), t[1].ljust(25),
                      t[2].ljust(25), t[3].ljust(25))
                for r in results:
                    print(r[1].ljust(25), r[2].ljust(25),
                          r[3].ljust(25), r[4].ljust(25))
        except Exception as e:
            print(e)
