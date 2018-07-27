# coding=utf-8
import urllib.request
import urllib
import requests
#from cookielib import CookieJar
import os
import re
import time


class ConnectWeb(object):
    def __init__(self):
        self.cookiejarinmemory = CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookiejarinmemory))
        urllib.request.install_opener(self.opener)
        self.username = ""
        self.password = ""

    def connect_baidu(self):
        try:
            urllib.request.urlopen("http://www.baidu.com", timeout=2)
            return 1
        except:
            return 0

    def login(self):
        try:
            post_url = ""
            form = {"action": "login", "username": self.username, "password": self.password, "ac_id": 4,
                    "user_ip": "", "nas_ip": "", "user_mac": "", "save_me": 1, "ajax": 1}
            fm1 = urllib.urlencode(form)
            page = urllib.request.urlopen(post_url, fm1).read()
        except Exception as e:
            self.disconnect()
            time.sleep(1)
            self.connect_wifi()

    def disconnect(self):
        os.system("netsh wlan disconnect")

    def wifis_nearby(self):
        p = os.popen("netsh wlan show all")
        content = p.read().decode("GB2312", "ignore")
        temp = re.findall(u"(SSID.*\n.*Network type.*\n.*\u8eab\u4efd\u9a8c\u8bc1.*\n.*\u52a0\u5bc6.*\n.*BSSID.*\n)",
                       content)
        result = []
        for i in temp:
            name = re.findall(u"SSID.*:(.*)\n", i)[0].replace(" ", "")
            result.append(name)
        return result

    def connect_wifi(self, name=None):
        os.system("netsh wlan connect name=%s" % name)

    def checking(self):
        while 1:
            try:
                if not self.connect_baidu():
                    self.login()
            except:
                pass
            time.sleep(10)

def get_status(url):
    try:
        r = requests.get(url, allow_redirects = False)
        status = r.status_code
        if status == 200:
            print('Network is ok')
            return 1
        else:
            print('Network error!!!!')
            return 0
    except:
        print('Network error!!!!')
        return 0
    #return r.status_code

#print(get_status('http://192.168.1.104/index.fcgi'))

def sleep(t):
    print('sleep %ss'%t)
    time.sleep(t)

if __name__ == "__main__":
    print('start')
    wifiList = ["sam5","APTest8"]
    #wifiList = ["SW-AC1200","haydn","sam5","Astrill","APTest8"]
    list = 0
    while True:
        sleep(10)
        wifiStatus = get_status('http://www.baidu.com')
        if wifiStatus == 0:
            os.system("netsh wlan connect name=%s" % wifiList[list])
            print('change network to %s'%wifiList[list])
            sleep(10)
            wifiStatus = get_status('http://www.baidu.com')
            if wifiStatus == 0:
                if list < len(wifiList):
                    list += 1
                else:
                    list = 0
        else:
            list = 0
    #test = ConnectWeb()
    #test.login()