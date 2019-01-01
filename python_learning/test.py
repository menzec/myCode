#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-27 09:55:45
# @Author  : ${menzec} (${menzc@outlook.com})
# @Link    : http://example.org
# @Version : $Id$

import os

path = r'D:\Code\NN_Model'
for fpathe, dirs, fs in os.walk(path):
    print(fpathe, dirs, fs)
