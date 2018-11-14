#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-16 23:15:40
# @Author  : ${menzec} (${menzc@outlook.com})
# @Link    : http://example.org
# @Version : $Id$

import requests
from scrapy import Selector
import MySQLdb

conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root',
                       passwd='123456', charset='utf8', db='proxy_pool')
cursor = conn.cursor()


class GetIp():

    def update_available_ip(self, ip, available):
        update_available_ip_sql = "update proxy_ip set available = '{0}' where ip = '{1}'".format(
            available, ip)
        cursor.execute(update_available_ip_sql)
        conn.commit()
        return True

    def delete_ip(self, ip):
        delete_ip_sql = "delete from proxy_ip where ip = '{0}'".format(ip)
        cursor.execute(delete_ip_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        # 判断给出的代理 ip 是否可用
        http_url = 'http://www.163.com/'
        proxy_url = 'http://{0}:{1}'.format(ip, port)

        print("proxy_url", proxy_url)
        try:
            proxy_dict = {
                'http': proxy_url
            }
            response = requests.get(http_url, proxies=proxy_dict)

        except Exception as e:
            print("[没有返回]代理 ip {0} 及 端口号 {1} 不可用，即将从数据库中删除".format(ip, port))
            # self.delete_ip(ip)
            self.update_available_ip(ip, '0')
            return False
        else:
            code = response.status_code
            if code >= 200 or code < 300:
                print("代理 ip {0} 及 端口号 {1} 可用".format(ip, port))
                html_doc = str(response.content, 'gbk')
                print(html_doc)
                return True
            else:
                print(
                    "[有返回，但是状态码异常]代理 ip {0} 及 端口号 {1} 不可用，即将从数据库中删除".format(ip, port))
                # self.delete_ip(ip)
                self.update_available_ip(ip, '0')
                return False

    def get_random_ip(self):

        select_random = '''
            select ip,port,speed,proxy_type from proxy_ip order by rand() limit 1
        '''

        cursor.execute(select_random)
        result = cursor.fetchone()
        ip = result[0]
        port = result[1]

        judge_re = self.judge_ip(ip, port)
        if judge_re:
            self.update_available_ip(ip, '1')
            return "http://{0}:{1}".format(ip, port)
        else:
            return self.get_random_ip()

    def crawl_ips(self):
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1"}
        for i in range(1, 2):
            response = requests.get(
                "http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
            selector = Selector(text=response.text)
            all_trs = selector.css("#ip_list tr")
            ip_list = []
            for tr in all_trs[1:]:
                speed_str = tr.css("td[class='country']")[2]
                title = speed_str.css(".bar::attr(title)").extract()[0]
                if title:
                    pass
                    speed = float(title.split("秒")[0])
                all_texts = tr.css("td::text").extract()
                print(all_texts)

                ip = all_texts[0]
                port = all_texts[1]
                attr = all_texts[4]
                type = all_texts[5]
                if attr == 'HTTPS' or attr == 'HTTP':
                    attr = '----------'
                    type = all_texts[4]

                ip_list.append((ip, port, speed, type))

            # 然后插入数据库
            for ip_info in ip_list:
                insert_sql = '''
                      insert into proxy_ip(ip,port,speed,proxy_type)
                      values('{0}','{1}','{2}','{3}')'''.format(ip_info[0], ip_info[1], ip_info[2], ip_info[3])

                print(insert_sql)
                cursor.execute(insert_sql)
                conn.commit()


if __name__ == '__main__':
    get_ip = GetIp()
    # get_ip.crawl_ips()
    # 随机地选择一个 proxy_ip
    for i in range(10):
        available_ip_port = get_ip.get_random_ip()
        print("可用的 ip 和端口号是：", available_ip_port)
