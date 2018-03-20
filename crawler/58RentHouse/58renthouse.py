# -*- coding:utf-8 -*-
import os
import time
import random
import requests
import sqlite3
# import pandas as pd
from time import sleep
from urllib import request
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

    @staticmethod
    def get_page(url):  # 获取链接中的网页内容
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        while True:
            try:
                req = request.Request(url=url, headers=headers)
                response = request.urlopen(req, timeout=30)
                page = response.read().decode('utf-8')
                return page
            except:
                sleep(40)
                continue

    def parse_brand(self, response):
        raise NotImplementedError

    def parse_body(self, response):
        """
        解析正文,由子类实现
        :param response: 爬虫返回的response对象
        :return: 返回经过处理的html正文文本
        """
        raise NotImplementedError


class RentHouse(Crawler):
    """
    """

    def parse_page_num(self, response):
        soup = BeautifulSoup(response.content, "html.parser")
        page = soup.find('div', {'class': 'pager'}).find_all('span')[-2]
        page_num = page.text
        return int(page_num)

    def parse_page_url(self, page_num):
        for n in range(1, page_num + 1):
            page_url = self.start_url + '/pn{}'.format(n)
            yield page_url

    def parse_url_info(self, page_url):
        # print(self.request(u).content.decode('utf-8'))
        # here need to use get_page() and 'lxml'
        soup = BeautifulSoup(self.get_page(page_url), 'lxml')
        for i in soup.find('ul', {'class': 'listUl'}).find_all('li'):
            try:
                name = i.select('h2 > a')[0].text.strip().replace(',', '')
            except:
                name = ''
            try:
                region = i.select('p > a')[0].text
            except:
                region = ''
            try:
                room = i.find('p', {'class': 'room'}).text.split(' ')
            except:
                room_type = ''
                room_type = ''
            else:
                room_type = room[0]
                room_size = room[-1].replace('\xa0\xa0\xa0\xa0', '')
            try:
                place = i.select('p > a')[1].text
            except:
                place = ''
            try:
                price = i.find('div', {'class': 'money'}).find('b').text
            except:
                price = ''
            info = {
                'name': name,
                'region': region,
                'place': place,
                'room_type': room_type,
                'room_size': room_size,
                'price': price,
            }
            yield info

    @staticmethod
    def save_csv():
        cars_info = pd.DataFrame([brand,title,boarding_time,km,discharge,sec_price,new_price]).T
        cars_info = cars_info.rename(columns={0:'Brand',1:'Name',2:'Boarding_time',3:'Km',4:'Discharge',5:'Sec_price',6:'New_price'})
        cars_info.to_csv('HouseData.csv', index=False)

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
        '''
        url1 = r'http://jxjump.58.com/service?target='
        url2 = 'FCADVFdVGJSbUnkeXUZDc90OcaCmJeAYtI2tEbrXHvqosdbzzm2F-DHb-XcgT9WSjAhmNnNrcdsX4saGuf70ZOoppuXhL2WHrTnZunpsfDaoMQ35jmmBUKMqI7mbQFBJxIZMOiVJI6ueRb3ypeB-UK1L3QXXw18Lt_r4Da1l6qTwKdt5yukPmMkDu62eFWvNPmTtZtfBlCHEPbBOOL46dYK_qEFT-1iM0Ga7-DrRipFBNCJa094-CSJ4Nvaoj08mTC5as&local=4&pubid=26180159&apptype=0&psid=198939924198617142114087231&entinfo=32658632817357_0&cookie=|||c5/njVpSFBkiXrqiEJxbAg==&fzbref=0&key=¶ms=jxzfbestpc'
        url = url1 + urllib.request.quote(url2)
        resp = urllib.request.urlopen(url)
        content = resp.read().decode('utf-8')
        print(content)
        '''
        title = ['name', 'region', 'place', 'room_type', 'room_size', 'price']
        page_num = self.parse_page_num(self.request(self.start_url))
        for url in self.parse_page_url(page_num):
            print(url)
            sleep(5 + random.uniform(0, 4))
            for info in self.parse_url_info(url):
                print(info)
                data = ','.join(info.get(v) for v in title)
                data = "\'" + data.replace(",", "\',\'") + "\'"
                k = ','.join(title)
                self.SQL(self.db_path, "INSERT INTO HOUSE ({}) VALUES ({})".format(k, data))
                #print(info)


if __name__ == "__main__":
    db_path = '{}/58house.db'.format(os.getcwd())
    if os.path.exists(db_path):
        os.remove(db_path)
    create_table = '''CREATE TABLE HOUSE
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
                        NAME           TEXT    NOT NULL,
                        REGION         TEXT    NOT NULL,
                        PLACE          TEXT    NOT NULL,
                        ROOM_TYPE      TEXT    NOT NULL,
                        ROOM_SIZE      TEXT    NOT NULL,
                        PRICE      TEXT    NOT NULL);'''

    #   'http://sz.58.com/chuzu/'   # no limit
    start_url = 'http://sz.58.com/zufang/'   # 整套出租
    crawler = RentHouse(db_path, start_url)
    crawler.SQL(db_path, create_table)
    crawler.run()
