#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-24 16:29:02
# @Author  : ${menzec} (${menzc@outlook.com})
# @Link    : http://example.org


import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import datetime
sys.path.append('..')
from Alexnet import alexnet
from Dataset import myDataset
from mynet import mymodel

Batch_Size = 256
Learning_Rate = 0.0002
All_Epoch = 100


def alexnet_UCMerced_main():
    startime = datetime.datetime.now()
    print('Start train alexnet,startime:%s' % (startime))
    # 定义是否使用GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #device = torch.device("cpu")
    print('device: ', device)
    datadir = r'D:\mendata\Data\UCMerced'
    modeldir = r'D:\mendata\Model\Alexnet-UCMerced'
    # 模型定义-
    train_alexnet = alexnet.Alexnet_UCMerced(
        len(myDataset.UCMerced.label())).to(device)
    # 超参数设置
    net_para = mymodel.Net_para(optimizer=optim.SGD(
        train_alexnet.parameters(), lr=Learning_Rate, momentum=0.9, weight_decay=5e-4), Batch_Size=int(Batch_Size / 32))
    data = myDataset.UCMerced(datadir, net_para.batch_size).getdata()
    train_net = mymodel.mzc_net(modeldir, data, net_para)
    train_net.pre_check(train_alexnet)
    parafile = open('%s/para.txt' % (modeldir), 'a')
    print('para.pre_epoch =%d\nBatch_Size = %d\nLearning_Rate = %f\nAll_Eoch = %d\n' % (
        train_net.para.pre_epoch, Batch_Size, Learning_Rate, All_Epoch), file=parafile)
    parafile.close()
    for epoch in range(train_net.para.pre_epoch, train_net.para.epoch):
        train_net.train(train_alexnet, epoch)
        train_net.test(train_alexnet, epoch)
    endtime = datetime.datetime.now()
    print('Alexnet UCMerced Training Finished! Endtime:%s, costtime:%s' %
          (endtime, endtime - startime))


def alexnet_cifar_main():
    startime = datetime.datetime.now()
    print('Start train alexnet,startime:%s' % (startime))
    # 定义是否使用GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #device = torch.device("cpu")
    print('device: ', device)
    datadir = r'D:\mendata\Data\cifar10'
    modeldir = r'D:\mendata\Model\Alexnet-cifar'
    # 模型定义-
    train_alexnet = alexnet.Alexnet_cifar(
        len(myDataset.myCifar10.label())).to(device)
    # 超参数设置
    net_para = mymodel.Net_para(optimizer=optim.SGD(
        train_alexnet.parameters(), lr=Learning_Rate, momentum=0.9, weight_decay=5e-4))
    data = myDataset.myCifar10(
        datadir, net_para.batch_size).getdata()
    train_net = mymodel.mzc_net(modeldir, data, net_para)
    train_net.pre_check(train_alexnet)
    parafile = open('%s/para.txt' % (modeldir), 'a')
    print('para.pre_epoch =%d\nBatch_Size = %d\nLearning_Rate = %f\nAll_Eoch = %d\n' % (
        train_net.para.pre_epoch, Batch_Size, Learning_Rate, All_Epoch), file=parafile)
    parafile.close()
    for epoch in range(train_net.para.pre_epoch, train_net.para.epoch):
        train_net.train(train_alexnet, epoch)
        train_net.test(train_alexnet, epoch)
    endtime = datetime.datetime.now()
    print('Alexnet cifar10 Training Finished! Endtime:%s, costtime:%s' %
          (endtime, endtime - startime))


if __name__ == '__main__':
    
    alexnet_cifar_main()
    #alexnet_UCMerced_main()
