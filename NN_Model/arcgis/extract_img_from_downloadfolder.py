#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-13 10:08:38
# @Author  : ${menzec} (${menzc@outlook.com})
# @Link    : http://example.org
# @Version : $Id$

import os
import shutil


def copy_image_to_counterpart_folder(img_folder, target_folder):
    img_name_list = os.listdir(img_folder)
    err_list = []
    finish_num = 0
    for img_name in img_name_list:
        img_dir_level = os.path.join(img_folder, img_name, img_name + '_大图')
        if not os.path.exists(img_dir_level):
            err_list.append(img_name)
            continue
        img_level = os.listdir(img_dir_level)
        for level in img_level:
            level_dir = os.path.join(img_dir_level, level)
            if not os.path.exists(level_dir):
                err_list.append(img_name + '-level')
            img_dir = os.path.join(level_dir, img_name + '.tif')
            target_level_dir = target_folder + '/' + level
            if not os.path.exists(target_level_dir):
                os.mkdir(target_level_dir)
            shutil.copyfile(img_dir, target_level_dir +
                            '/' + img_name + '.tif')
    with open(target_folder + '/err_log.txt','w') as err_fn:
        err_fn.write(err_list)
        del err_list
        err_list = []


def main():
    img_folder = r'D:\SGDownload\google_airport'
    target_folder = r'D:\data\airport'
    copy_image_to_counterpart_folder(img_folder, target_folder)

if __name__ == '__main__':
    main()
