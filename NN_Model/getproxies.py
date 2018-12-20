import requests
from bs4 import BeautifulSoup
import bs4
import pdb


class getProxies(object):
    """docstring for getIP"""

    def __init__(self, speed_threshold=1.5, circle=10):
        super(getProxies, self).__init__()
        self.base_url = 'http://www.xicidaili.com/wt/'
        self.speed_threshold = speed_threshold
        self.courrent_ip_list_num = 0
        self.circle = circle
        self.proxies_list = []

    def getHtmlText(self, url):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'}
        try:
            r = requests.get(url, timeout=10, headers=headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            return ''

    def fillIpList(self, html):
        info_list = []
        soup = BeautifulSoup(html, 'html.parser')
        # pdb.set_trace()
        for tr in soup.find('table').children:
            if isinstance(tr, bs4.element.Tag):
                tds = tr('td')
                if len(tds) < 7:
                    continue
                divs = tr('div')
                info_list.append(
                    [tds[5].string, tds[1].string, tds[2].string, float(divs[0].attrs['title'][:-2])])
        return info_list

    def makeProxies(self, info_list, speed_threshold=1.5):
        proxies = []
        for http, ip, port,  speed in info_list:
            if speed < speed_threshold:
                proxies.append({http: ip + ':' + port})
        return proxies

    def get_proxy(self):
        if len(self.proxies_list) == 0:
            self.courrent_ip_list_num += 1
            if self.courrent_ip_list_num > self.circle:
                self.courrent_ip_list_num = 1
            url = self.base_url + str(self.courrent_ip_list_num)
            html = self.getHtmlText(url)
            ip_list = self.fillIpList(html)
            self.proxies_list = self.makeProxies(ip_list)
        return self.proxies_list.pop(0)


def main():
    # 实例化对象
    prox = getProxies()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'}
    testurl = 'http://www.baidu.com'
    corr = 0
    temp = 0
    for i in range(500):
        # 调用生成代理函数
        proxy = prox.get_proxy()
        r = requests.get(testurl, headers=headers, proxies=proxy)
        if temp != prox.courrent_ip_list_num:
            temp = prox.courrent_ip_list_num
            print(len(prox.proxies_list))
            print(prox.courrent_ip_list_num)
        if r.status_code == 200:
            corr += 1
    print(corr)


if __name__ == '__main__':
    # test founction
    main()
