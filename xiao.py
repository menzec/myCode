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
mystr = '我爱你中国'
print(len(mystr))
print(type(mystr))
mystr_utf8 = mystr.encode(encoding='utf-8')
print(len(mystr_utf8))
print(type(mystr_utf8))