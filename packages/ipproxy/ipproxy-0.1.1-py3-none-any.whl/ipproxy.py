import requests

from lxml import etree

import datetime

import random


class Proxy:
    def __init__(self, choice=20):
        self.choice = choice
        self.proxies = self.get_proxies()
        self.proxy = self.proxies.get("proxy")

    def send_request(self, page):
        base_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(page)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
        response = requests.get(base_url, headers=headers)
        data = response.content.decode()
        return data

    def get_proxies(self):
        for c in range(self.choice):
            page = random.randint(1, 10)
            data = self.send_request(page)
            if data == '-10\n':
                continue

            html_data = etree.HTML(data)
            parse_list = html_data.xpath('/html/body/div[3]/main/div/section/div[3]/div[1]/table/tbody/tr')
            row = random.randint(0, len(parse_list) - 1)
            tr = parse_list[row]
            proxies = {}
            http_type = ''.join(tr.xpath('./td[4]/text()')).lower()
            ip = ''.join(tr.xpath('./td[1]/text()'))
            port = ''.join(tr.xpath('./td[2]/text()'))
            proxies["proxy"] = {http_type: f"{http_type}://{ip}:{port}"}
            proxies["anonymous"] = ''.join(tr.xpath('./td[3]/text()'))
            proxies["location"] = ''.join(tr.xpath('./td[5]/text()'))
            proxies["speed"] = ''.join(tr.xpath('./td[6]/text()'))
            proxies["time"] = ''.join(tr.xpath('./td[7]/text()'))
            proxies["free"] = ''.join(tr.xpath('./td[8]/text()'))
            date_str = proxies['time']
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            now = datetime.datetime.now()
            time_diff = now - date_obj

            speed = float(proxies["speed"][:-1])
            if time_diff.days < 10 and speed < 1:
                break

        return proxies

    def get_proxy(self):
        return self.proxy

