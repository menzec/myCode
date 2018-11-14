#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-06 12:59:14
# @Author  : ${menzec} (${menzc@outlook.com})
# @Link    : http://example.org
# @Version : $Id$

import os
import sys
import math
import time
import datetime
import requests
import urllib3
from PIL import Image
from bs4 import BeautifulSoup
import bs4
import multiprocessing
import pdb
import random
import string
# 墨卡托投影坐标系
# 墨卡托投影以整个世界范围，赤道作为标准纬线，本初子午线作为中央经线，两者交点为坐标原点，
# 向东向北为正，向西向南为负。南北极在地图的正下、上方，而东西方向处于地图的正右、左
# 由于Mercator Projection在两极附近是趋于无限大，
# 因此它并没完整展现整个世界，地图上最高纬度是85.05度。为了简化计算，我们采用球形映射，而不是椭球体形状
# 由于赤道半径为6378137米，则赤道周长为2*PI*r = 40073834.771，因此Y轴的取值范围：[-20037508.3427892,20037508.3427892]。
# 当纬度φ接近两极，即90°时，X值趋向于无穷。因此通常把X轴的取值范围也限定在[-20037508.3427892,20037508.3427892]之间
# 墨卡托投影坐标系（米）下的坐标范围是：
# 最小为(-20037508.3427892, -20037508.3427892 )到最大 坐标为(20037508.3427892,20037508.3427892)
# 不同等级对应的分辨率
# leve 0:156543.034
# leve 1:78271.517
# leve 2:39135.758
# leve 3:19567.879
# leve 4:9783.940
# leve 5:4891.970
# leve 6:2445.985
# leve 7:1222.992
# leve 8:611.496
# leve 9:305.748
# leve 10:152.874
# leve 11:76.437
# leve 12:38.219
# leve 13:19.109
# leve 14:9.555
# leve 15:4.777
# leve 16:2.389
# leve 17:1.194
# leve 18:0.597
# leve 19:0.299
# leve 20:0.149
# leve 21:0.075
# leve 22:0.037


class URL_Error(Exception):
    """docstring for  My_Error"""

    def __init__(self, errinfo):
        super(URL_Error, self).__init__()
        self.err_info = errinfo

    def __repr__(self):
        return self.err_info


class Size_Error(Exception):
    """docstring for  HTTPError"""

    def __init__(self, errinfo):
        super(Size_Error, self).__init__()
        self.err_info = errinfo

    def __repr__(self):
        return self.err_info


def leve_to_resolution(n):
    return 20037508.3427892 * 2 / 256 / math.pow(2, n)


def generate_random_str(randomlength=16):
    """
    生成一个指定长度的随机字符串，其中
    string.digits=0123456789
    string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    str_list = [random.choice(string.digits + string.ascii_letters)
                for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str


def longLat_to_tile(longtitude, latitude, room):
    n = math.pow(2, room)
    tileX = (longtitude + 180) / 360 * n
    tileY = (1 - (math.log(math.tan(math.radians(latitude)) +
                           (1 / math.cos(math.radians(latitude)))) / math.pi)) / 2 * n
    return (tileX, tileY)
# 具体含义如下：
# m：路线图
# t：地形图
# ​p：带标签的地形图
# ​s：卫星图
# y：带标签的卫星图
# ​h：标签层（路名、地名等）
# eg:http://www.google.cn/maps/vt/lyrs=s&gl=en&x=27006&y=12470&z=15
# 名称:    www.google.cn
# Addresses:  203.208.50.56
#           203.208.50.63
#           203.208.50.55
#           203.208.50.47
#    http://mt1.google.cn/vt/lyrs=s&hl=en&gl=cn&x=27006&y=12470&z=15
# 名称:    mt1.google.cn
# Addresses:  203.208.43.111
#           203.208.43.127
#           203.208.43.119
#           203.208.43.120
# 注意：gl = en gl=cn 返回的地图不一致


class getProxies(object):
    """docstring for getIP"""

    def __init__(self, speed_threshold=1.5, start=0, circle=10, primary_proxies=None):
        super(getProxies, self).__init__()
        self.base_url = 'http://www.xicidaili.com/wt/'
        self.speed_threshold = speed_threshold
        self.courrent_ip_list_num = start
        self.circle = circle
        self.primary_proxies = primary_proxies
        self.proxies_list = []

    def getHtmlText(self, url):
        headers = {
            'user-agent': 'Chrome/67.0.3396.62 Safari/537.36', 'Connection': 'close'}
        try:
            r = requests.get(url, timeout=10, headers=headers,
                             proxies=self.primary_proxies)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            print(r.request.headers)
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


def download_tile(tileX, tileY, zoom, base_url, map_type='s', proxies=None):
    map_paras = {
        "lyrs": map_type,
        'gl': 'en',
        'x': str(tileX),
        'y': str(tileY),
        'z': str(zoom),
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
        'Connection': 'close',
    }
    try:
        r = requests.get(base_url, params=map_paras,
                         headers=headers, proxies=proxies)
        r.raise_for_status()
        img = r.content
        r.close()
    except requests.HTTPError:
        # print('Error!\ntileX = %d ,tileY = %d ,zoom = %d failed!' %
        #       (tileX, tileY, zoom))
        raise URL_Error('HTTPError')
    return img


def change_url(base_urls, proxies, cur_url, cur_proxy):
    # base_urls.append([base_urls.pop(0)[0], time.time()])
    # print('change_urls')
    # if time.time() - base_urls[0][1] < 600:
    #     print('rest 600s')
    #     time.sleep(600)
    if cur_url == base_urls[-1][0]:
        cur_proxy = proxies.get_proxy()
    for i in range(len(base_urls)):
        if cur_url == base_urls[i][0]:
            if i == len(base_urls) - 1:
                url = base_urls[0][0]
            else:
                url = base_urls[i + 1][0]
    return (url, cur_proxy)


def download_single_image(tile_coor, zoom, size, base_url, proxies=None):
    image_temp_name = generate_random_str(10)
    image_list = []
    x_step = size[0] / 256  # 该方向上占据几个瓦片(裁剪后)
    y_step = size[1] / 256
    # 各方向实际需要下载几个瓦片
    x_tile_num = int(tile_coor[0] + x_step / 2) + \
        1 - int(tile_coor[0] - x_step / 2)
    y_tile_num = int(tile_coor[1] + y_step / 2) + \
        1 - int(tile_coor[1] - y_step / 2)
    for y in range(int(tile_coor[1] - y_step / 2), int(tile_coor[1] + y_step / 2) + 1):
        for x in range(int(tile_coor[0] - x_step / 2), int(tile_coor[0] + x_step / 2) + 1):
            if base_url:
                image_list.append(download_tile(
                    x, y, zoom, base_url, proxies=proxies))
    # 拼接下载的瓦片
    merge_image = Image.new(
        'RGB', (256 * x_tile_num, 256 * y_tile_num))
    for i in range(len(image_list)):
        with open(image_temp_name, 'wb') as f:
            f.write(image_list[i])
        fromImge = Image.open(image_temp_name)
        loc = ((i % x_tile_num) * 256, int(i / x_tile_num) * 256)
        merge_image.paste(fromImge, loc)
    os.remove(image_temp_name)
    # 裁剪拼接的瓦片
    box = (int(256 * (tile_coor[0] - x_step / 2 - int(tile_coor[0] - x_step / 2))),
           int(256 * (tile_coor[1] - y_step / 2 -
                      int(tile_coor[1] - y_step / 2))),
           size[0] + int(256 * (tile_coor[0] - x_step /
                                2 - int(tile_coor[0] - x_step / 2))),
           size[1] + int(256 * (tile_coor[1] - y_step / 2 -
                                int(tile_coor[1] - y_step / 2)))
           )
    crop_image = merge_image.crop(box)
    return crop_image


def batch_download_image(filename, img_save_dir, zoom, size, base_urls=None, proxies=None):
    with open(filename, 'r') as fp:
        ferr = open('%s_error%s' % (filename[:-4], filename[-4:]), 'w')
        logfile = open('%s/log.txt' % (img_save_dir), 'w')
        i = 0
        err_num = 0
        file_size = 0
        # proxies = getProxies()
        cur_proxy = proxies.get_proxy()
        cur_url = base_urls[0][0]
        cur_url, cur_proxy = change_url(base_urls, proxies, cur_url, cur_proxy)
        coor_info = fp.readlines()
        num = len(coor_info)

        # num = int(fp.readline())  # 跳过表示个数的第一行
        # size_str = fp.readline()  # 尺寸信息
        x_length, y_length = size
        # x_length = int(size_str[:size_str.find(',')])
        # y_length = int(size_str[size_str.find(',') + 1:])
        # data = fp.readline()
        print('file %s has %d coordinates.' %
              (os.path.basename(filename), num))
        for data in coor_info:
            try:
                # cur_url = base_urls[0][0]
                i += 1
                longtitude = float(data[:data.find(',')])
                latitude = float(data[data.find(',') + 1:])
                image_name = '%s/Z%s_L%s_B%s.png' % (
                    img_save_dir, str(zoom), str(longtitude), str(latitude))
                # data = fp.readline()
                if os.path.exists(image_name):
                    # print('%d/%d %s exist, skip!' %
                    #       (i, num, os.path.basename(image_name)))
                    continue
                tile_coor = longLat_to_tile(longtitude, latitude, zoom)
                img = download_single_image(
                    tile_coor, zoom, (x_length, y_length), base_url=cur_url, proxies=cur_proxy)
                img.save(image_name)
                print(datetime.datetime.now(),
                      'Download %d/%d pictures,succeed!' % (i, num), file=logfile)
                file_size += os.path.getsize(image_name)
                if file_size > 10000000:
                    file_size = 0
                    # change_url(base_urls)
                    cur_url, cur_proxy = change_url(
                        base_urls, proxies, cur_url, cur_proxy)
            except URL_Error as err:
                err_num += 1
                ferr.write('%f,%f\n' % (longtitude, latitude))
                ferr.flush()
                # print('err_num %d: Download %d/%d pictures failed!\t%f,%f' %
                #       (err_num, i, num, longtitude, latitude))
                print('err_num %d: Download %d/%d pictures failed!\t%f,%f' %
                      (err_num, i, num, longtitude, latitude), file=logfile)
            except (urllib3.exceptions.MaxRetryError, urllib3.exceptions.MaxRetryError,
                    requests.exceptions.ChunkedEncodingError, urllib3.exceptions.ProtocolError,) as err:
                print(err, '\nMaxRetryError/MaxRetryError Error!')
                print(err, '\nMaxRetryError/MaxRetryError Error!', file=logfile)
                # change_url(base_urls)
                cur_url, cur_proxy = change_url(
                    base_urls, proxies, cur_url, cur_proxy)
                file_size = 0
                # time.sleep(600)
        ferr.close()
    if not os.path.getsize('%s_error%s' % (filename[:-4], filename[-4:])):
        os.remove('%s_error%s' % (filename[:-4], filename[-4:]))
    print(datetime.datetime.now(), filename + 'Finish')


def main():
    zoom = 16
    size = (128, 128)
    base_urls = [
        ['http://mt2.google.cn/vt', time.time()],
        ['http://mt1.google.cn/vt', time.time()],
        ['http://mt0.google.cn/vt', time.time()],
        ['http://www.google.cn/maps/vt', time.time()],
    ]
    download_file_dir = r"D:\data\qinghua\downloadfile"
    save_dir = r'D:\data\qinghua\img'
    # download_file_dir = r"D:\data\qinghua\test"
    # save_dir = r'D:\data\qinghua\test\img'
    download_files = os.listdir(download_file_dir)
    starttime = time.time()
    i = 450
    m = 1
    processes = []
    a_proxies = getProxies(start=5)
    for file in download_files:
        if os.path.splitext(file)[1] != '.txt' or file[-9:] == 'error.txt':
            continue
        cur_save_dir = '%s/%s' % (save_dir, os.path.splitext(file)[0])
        cur_download_file = '%s/%s' % (download_file_dir, file)
        if not os.path.exists(cur_save_dir):
            os.mkdir(cur_save_dir)
        proxy = a_proxies.get_proxy()
        proxies = getProxies(start=i, primary_proxies=proxy)
        print('%s start %d process' % (file, m))
        p = multiprocessing.Process(target=batch_download_image, args=(
            cur_download_file, cur_save_dir, zoom, size, base_urls, getProxies(start=i)))
        i += 10
        m += 1
        p.start()
        time.sleep(10)
        processes.append(p)
    for p in processes:
        p.join()

    print('All Finish')

if __name__ == '__main__':
    main()
