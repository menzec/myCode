#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-27 20:42:17
# @Author  : ${menzec} (${menzc@outlook.com})
# @Link    : http://example.org
# @Version : $Id$

# import jieba
# g_mode = "default"


# def cut_jigou_name(jigou_name):
#     bowl = []  # 定义一个空列表，用于存放分割出的后边部分
#     houzhui = ["大学", "学院", "医院", "中心", "中学", "中专", "同盟", "集团", "师专", "师范", "油田", "政府", "基地", "杂志", "高专", "车间", "高中", "小学", "机构", "园地", "石化""厂", "系", "所", "室", "处", "站", "馆", "局", "组", "队",
#                "科", "委", "行", "厅", "会", "校", "场", "台", "班", "办", "区", "园", "社", "分公司",
#                "级", "业", "点", "署", "团", "排", "连", "师", "段"]
#     global g_mode
#     cut = jieba.cut(jigou_name)  # 用jieba分词器把这个字符串分割
#     fencihou = ','.join(cut)  # 分割后的词用，连接
#     wangxiao = list(fencihou)  # 把连接后的词列表化,之后能够获取字符的索引
#     result = jieba.tokenize(fencihou)  # 获取分词后各个词语及他们的开始位置和结束位置
# # 下边这个循环用来判断这个机构名中有几个机构的后缀 ，并在这些后缀后面插入分割线/
#     geshu = 0
#     for tk in result:
#         #         print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))
#         for i in houzhui:
#             if i in tk[0]:
#                 n = tk[2]
#                 geshu += 1
#                 n = n + geshu - 1
#                 wangxiao.insert(n, "/")
# ###
#     str_2 = ''.join(wangxiao)  # 把列表再转回字符串
#     if "," in str_2:  # 清除，
#         str_2 = str_2.replace(",", "")
#     jiaxiexian = str_2.split("/")
#     mytest = [i for i in jiaxiexian if i != '']
#     return (mytest)
# # 清除符号
# import re
# filename = r"C:\SoftWare/all_organ"
# writename = r"C:\SoftWare/fuhao_qingchu.txt"
# originname = r"C:\SoftWare/origin.txt"
# i = 0.0
# j = 0.0
# with open(filename, "r", encoding="UTF-8") as fn:
#     with open(writename, "w", encoding="UTF-8") as wn:
#         with open(originname, "w", encoding="UTF-8") as orn:
#             line = fn.readline()
#             while line:
#                 orn.write(line)
#                 if re.search("[!@#$%^&*/\\;:,?`.·！￥：；,，\(\)、]", line):
#                     new_line = re.sub(
#                         "[!@#$%^&*/\\;:,?`.·！￥：；,，\(\)、]", "", line)
#                     wn.write(new_line)
#                     i += 1
#                 else:
#                     wn.write(line)
#                 j += 1
#                 line = fn.readline()
#                 if j % 10000 == 0:
#                     wn.flush()
#                     print(i, '  finish')
#                     print('有符号行数', i, '总行数', j)
#                     break
#             print("结束")
# # if __name__ == '__main__':
#     datafile = r'C:\Users\Menzec\Documents\WeChat Files\menzec\Files\file_s1.csv'
#     placefile = r'D:\data\1.txt'
#     postfix = r'D:\data\2.txt'
#     i = 0.0
#     with open(datafile, 'r', encoding='UTF-8') as dataf:
#         with open(placefile, 'w', encoding='UTF-8') as pf:
#             with open(postfix, 'w', encoding='UTF-8') as postf:
#                 str_data = dataf.readline()
#                 while str_data:
#                     cut_str = cut_jigou_name(str_data)
#                     pf.write(str(cut_str[0]) + '\n')
#                     postdata = cut_str[1:]
#                     for strtmp in postdata:
#                         postf.write(strtmp.replace('\n', '') + ',')
#                     postf.write('\n')
#                     i += 1
#                     if i % 10000 == 0:
#                         print(i, 'finish')
#                         pf.flush()
#                         postf.flush()
#                         break
#                     str_data = dataf.readline()
#                 print('finish')
# 把没符号的追加进去
# filename = r"D:\data\jieguo02.txt"
# writename = r"D:\data\test_origin.txt"
# i = 0.0
# with open(filename, "r", encoding="UTF-8") as fn:
#      with open(writename, "w", encoding="UTF-8") as wn:
#         line =fn.readline()
#         for dd in range(245600):
#             line =fn.readline()
#         for jj in range(1000):
#             line =fn.readline()
#             wn.write(line)
# with open(filename, "r", encoding="UTF-8") as fn:
#     with open(writename, "a", encoding="UTF-8") as wn:
#         line = fn.readline()
#         while line:
#             flag = 0
#             if re.search("[!@#$%^&*/\\;:,?`.·！￥：；\(\)、]", line):
#                 flag = 1
#             else:
#                 wn.write(line)
#                 i += 1
#                 if i % 10000 == 0:
#                     wn.flush()
#                     print(i, '  finish')
#             line = fn.readline()
#         print(i)
#         print("结束")
# mystr = '我爱你中国'
# print(len(mystr))
# print(type(mystr))
# mystr_utf8 = mystr.encode(encoding='utf-8')
# print(len(mystr_utf8))
# print(type(mystr_utf8))
import requests
from bs4 import BeautifulSoup
import os
import re
import bs4
s = requests.Session()
url = 'https://baike.baidu.com/item/%E4%BC%8A%E9%80%9A%E7%81%AB%E5%B1%B1%E7%BE%A4%E5%9B%BD%E5%AE%B6%E7%BA%A7%E8%87%AA%E7%84%B6%E4%BF%9D%E6%8A%A4%E5%8C%BA/8758896'
# Cookie  = 'BIDUPSID=B3F8382F59B7C5BAC977700953703BC1; PSTM=1510409949; BAIDUID=018D8A7A013359893B1066ABAE61853A:FG=1; __cfduid=d92ac5c0d7dea35057f395a9a7b2b2b951525274842; BDUSS=HdyTEpkekxMZzJINlA0LW0ybUh0ZmFVMDNFWjR0dTNPZ2xxaWltR0V3eXNVSHBiQVFBQUFBJCQAAAAAAAAAAAEAAADCr1J1u~rWx7XE5ue087TzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKzDUlusw1JbN; delPer=0; pgv_pvi=4423961600; pgv_si=s4874264576; BDRCVFR[nnelRoIzZZm]=mk3SLVN4HKm; PSINO=1; MCITY=-%3A; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; ZD_ENTRY=baidu; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1542679052,1542683848,1542698420,1542699539; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1542699539; H_PS_PSSID=1441_21112_27509'
# User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
# Referer = 'https://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E8%87%AA%E7%84%B6%E4%BF%9D%E6%8A%A4%E5%8C%BA'
# headers = {'Cookie':Cookie,'User-Agent':User_Agent,'Referer':Referer}
s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
r = s.get(url)
r.encoding = 'gbk2312'
rawhtml = r.text
soup = BeautifulSoup(rawhtml, 'html.parser')
main = soup.find(attrs = {"class":"main-content"})



num = 0
info = []
for i in main.contents:  
    try:
        if i.attrs['class'] == ['para-title', 'level-2']:
            print(i)
            print(num)
            info.append(num)
    except (KeyError,AttributeError) as err:
        pass
        continue
    num+=1
print(info)
print(main.contents[info[0]])