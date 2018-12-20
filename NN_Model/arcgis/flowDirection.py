#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-04 10:10:25
# @Author  : ${menzec} (${menzc@outlook.com})
# @Link    : http://example.org
# @Version : $Id$

import os
import numpy as np
import math

class Flow_Direction(object):
    """docstring for flowDirection"""

    def __init__(self, input_img, max_value= 999999,directionValue=np.array([[32, 64, 128], [16, -1, 1], [8, 4, 2]])):
        # class inhert,ignore
        super(Flow_Direction, self).__init__()
        # Class member variables
        self.direction_code_array = directionValue
        self.input_img = input_img
        self.max_value = max_value

    def calDirection(self, dirValue):
        '''计算输入3*3矩阵中心值的流向'''
        rows, cols = dirValue.shape
        center_value = dirValue[1, 1]
        # print('center_value:%d' % (center_value))
        distance = 0.0
        max_distance = 0.0
        max_postion = [0, 0]
        for row in range(rows):
            for col in range(cols):
                if dirValue[row, col] < center_value:
                    # pdb.set_trace()
                    distance = (
                        center_value - dirValue[row, col]) / math.sqrt(((row - 1) * (row - 1) + (col - 1) * (col - 1)))
                    if distance > max_distance:
                        max_distance = distance
                        max_postion = [row, col]
                    # print('distance:', distance, row, col)
        # 如果没有填挖或者是平原,返回-1
        # if max_distance == 0:
        #     return -1
        # print('max_distance', max_distance)
        # print('max_postion:', max_postion)
        # direction = self.direction_code_array[max_postion[0], max_postion[1]]
        # print('direction:', direction)
        return self.direction_code_array[max_postion[0], max_postion[1]]

    def flow_Direction(self):
        in_img = self.input_img
        rows, cols = in_img.shape
        # 定义的扩展后的矩阵，周围用一个极值填充
        cal_img = np.zeros(
            (rows + 2, rows + 2), dtype='float32')
        # 存储流向方向
        out_diretion_array = np.zeros((in_img.shape), dtype='int32')
        # 临时存储3*3的矩阵
        sub_cal = np.zeros((3, 3), dtype=cal_img.dtype)
        # 将输入影像的值赋值给扩展后的矩阵
        cal_img[1:rows + 1, 1:cols + 1] = in_img
        # 填充极值
        cal_img[0, :] = self.max_value
        cal_img[rows + 1, :] = self.max_value
        cal_img[:, 0] = self.max_value
        cal_img[:, cols + 1] = self.max_value
        # 循环计算每个像元的流向值
        for row in range(1, rows + 1):
            for col in range(1, cols + 1):
                # 取3*3局矩阵
                sub_cal= cal_img[row-1:row+2,col-1:col + 2]
                # 计算流向
                direction = self.calDirection(sub_cal)
                out_diretion_array[row - 1, col - 1] = direction
        return out_diretion_array


def flowDirection(in_img):
    return Flow_Direction(in_img).flow_Direction()


def main():
    in_img = np.array([[78, 72, 69, 71, 58, 49],
                       [74, 67, 56, 49, 46, 50],
                       [69, 53, 44, 37, 38, 48],
                       [69, 58, 55, 22, 31, 24],
                       [68, 61, 47, 21, 16, 19],
                       [74, 53, 34, 12, 11, 12]])
    out = flowDirection(in_img)
    print(out)

if __name__ == '__main__':
    main()
