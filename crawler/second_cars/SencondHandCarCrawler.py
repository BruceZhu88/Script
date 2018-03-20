# -*- coding:utf-8 -*-
import os
import time
import random
import requests
import sqlite3
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Crawler(object):
    """
    爬虫基类，所有爬虫都应该继承此类
    """
    name = None

    def __init__(self, db_path, start_url):
        """
        """
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
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
        }
        status = 0
        while status != 200:
            response = requests.get(url, headers=headers, **kwargs)
            status = response.status_code
            if status == 200:
                break
            print('Waiting 45s')
            time.sleep(45)
        return response

    def parse_brand(self, response):
        raise NotImplementedError

    def parse_body(self, response):
        """
        解析正文,由子类实现
        :param response: 爬虫返回的response对象
        :return: 返回经过处理的html正文文本
        """
        raise NotImplementedError


class SecondHandCarCrawler(Crawler):
    """
    """

    def parse_brand_list(self, response):
        soup = BeautifulSoup(response.content, "html.parser")
        brand_list = soup.find_all('div', {'class': 'brand-name'})
        for l in brand_list:
            yield l

    def parse_brand(self, brand_list):
        for a in brand_list.find_all('a'):
            brand_name = a.text
            url = a.get("href")
            if not url.startswith("http"):
                url = "".join([self.domain, url])
            yield brand_name, url

    def parse_target_url(self, brand_url):
        response = self.request(brand_url)
        soup = BeautifulSoup(response.content, "html.parser")
        if len(soup.find_all('div', {'class': 'the-pages'})) == 0:
            pages = 1
        else:
            pages = int([page.text for page in soup.find_all(
                'div', {'class': 'the-pages'})[0].find_all('a')][-2])
        time.sleep(3)

        for i in range(1, pages + 1):
            url = '{}?page={}#pagetag'.format(brand_url, str(i))
            yield url

    def parse_info(self, brand, page_url):
        response = self.request(page_url)
        soup = BeautifulSoup(response.content, "html.parser")
        try:
            for items in soup.find_all('div', {'class': 'item_details'}):
                info = items.find_all('li')
                infos = {
                    'brand': brand,
                    'name': items.find('a')['title'],
                    'boarding_time': info[0].text[4:],
                    'km': info[1].text[4:],
                    'discharge': info[3].text[4:],
                    'sec_price': items.parent.find(class_='heji').
                    text.replace(',', ''),  # e.g 2,667 = 2667
                    'new_price': items.parent.find('del').text.replace(',', '')
                }
                yield infos
        except Exception as e:
            print(e)
            pass

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

    def run(self):
        title = ['brand', 'name', 'boarding_time', 'km',
                 'discharge', 'sec_price', 'new_price']
        for brands_list in self.parse_brand_list(self.request(self.start_url)):
            for brand, brand_url in self.parse_brand(brands_list):
                for page_url in self.parse_target_url(brand_url):
                    for info in self.parse_info(brand, page_url):
                        data = ','.join([info.get(value)
                                         for value in title])
                        data = "\'" + data.replace(",", "\',\'") + "\'"
                        print(data)
                        self.SQL(self.db_path, "INSERT INTO CAR (BRAND,NAME,BOARDING_TIME,KM, \
                            DISCHARGE,SEC_PRICE,NEW_PRICE) \
                            VALUES ({})".format(data))
                    time.sleep(3 + random.uniform(1, 3))
                    # return


if __name__ == "__main__":
    db_path = '{}/second_cars_info.db'.format(os.getcwd())
    if os.path.exists(db_path):
        os.remove(db_path)
    create_table = '''CREATE TABLE CAR
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
                        BRAND           TEXT    NOT NULL,
                        NAME            TEXT    NOT NULL,
                        BOARDING_TIME   TEXT    NOT NULL,
                        KM              TEXT    NOT NULL,
                        DISCHARGE       TEXT    NOT NULL,
                        SEC_PRICE       TEXT    NOT NULL,
                        NEW_PRICE       TEXT    NOT NULL);'''
    start_url = 'http://shanghai.taoche.com/all/'
    crawler = SecondHandCarCrawler(db_path, start_url)
    crawler.SQL(db_path, create_table)
    crawler.run()
