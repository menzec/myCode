#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-10 10:42:58
# @Author  : ${menzec} (${menzc@outlook.com})
# @Link    : http://example.org
# @Version : $Id$

import os
import shutil


def copylog(rootdir, targetdir):
    alldir = os.listdir(rootdir)
    for path in alldir:
        olddir = rootdir + '/' + path + '/' + 'log'
        newdir = targetdir + '/' + path
        shutil.copytree(olddir, newdir)
        print('copy %s to %s ...'%(olddir, newdir))
        
def main():
    rootdir  = r'D:\data\log\cifar'
    targetdir = r'D:\NGCC\deep_learning\新建文件夹\cifar_all'
    copylog(rootdir,targetdir)

if __name__=='__main__':
    main()
