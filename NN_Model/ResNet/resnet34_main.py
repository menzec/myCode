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
from ResNet import resnet
from Dataset import myDataset
from mynet import mymodel

Batch_Size = 128
Learning_Rate = 0.001
All_Epoch = 150


def resnet34_cifar_main():
    startime = datetime.datetime.now()
    print('Start train resnet18_cifar_main,startime:%s' % (startime))
    # 定义是否使用GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #device = torch.device("cpu")
    print('device: ', device)
    #wkdir = os.getcwd()
    datadir = r'D:\data\cifar10'
    modeldir = r'D:\data\Model\resnet18'
    # 模型定义-ResNet
    renet34 = resnet.ResNet34(len(myDataset.myCifar10.label())).to(device)
    # 超参数设置
    net_para = mymodel.Net_para(optimizer=optim.SGD(
        renet34.parameters(), lr=Learning_Rate, momentum=0.9, weight_decay=5e-4))
    data = myDataset.myCifar10(datadir, net_para.batch_size).getdata()
    train_net = mymodel.mzc_net(modeldir, data, net_para)
    train_net.pre_check(renet34)
    parafile = open('%s/para.txt' % (modeldir), 'a')
    print('para.pre_epoch =%d\nBatch_Size = %d\nLearning_Rate = %f\nAll_Eoch = %d\n' % (
        train_net.para.pre_epoch, Batch_Size, Learning_Rate, All_Epoch), file=parafile)
    parafile.close()
    for epoch in range(train_net.para.pre_epoch, train_net.para.epoch):
        train_net.train(renet34, epoch)
        train_net.test(renet34, epoch)
    endtime = datetime.datetime.now()
    print('ResNet34 Training Finished! Endtime:%s, costtime:%s' %
          (endtime,  endtime - startime))


def resnet34_UCMerced_main():
    startime = datetime.datetime.now()
    print('Start train resnet18_UCMerced_main,startime:%s' % (startime))
    # 定义是否使用GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #device = torch.device("cpu")
    print('device: ', device)
    #wkdir = os.getcwd()
    datadir = r'D:\data\UCMerced'
    modeldir = r'D:\data\Model\resnet34'
    # 模型定义-ResNet
    renet34 = resnet.ResNet34_UCMerced(
        len(myDataset.UCMerced.label())).to(device)
    # 超参数设置
    net_para = mymodel.Net_para(optimizer=optim.SGD(
        renet34.parameters(), lr=Learning_Rate, momentum=0.9, weight_decay=5e-4), Batch_Size=int(Batch_Size / 4))
    data = myDataset.UCMerced(datadir, net_para.batch_size).getdata()
    train_net = mymodel.mzc_net(modeldir, data, net_para)
    train_net.pre_check(renet34)
    parafile = open('%s/para.txt' % (modeldir), 'a')
    print('para.pre_epoch =%d\nBatch_Size = %d\nLearning_Rate = %f\nAll_Eoch = %d\n' % (
        train_net.para.pre_epoch, Batch_Size, Learning_Rate, All_Epoch), file=parafile)
    parafile.close()
    for epoch in range(train_net.para.pre_epoch, train_net.para.epoch):
        train_net.train(renet34, epoch)
        train_net.test(renet34, epoch)
    endtime = datetime.datetime.now()
    print('ResNet34 Training Finished! Endtime:%s, costtime:%s' %
          (endtime,  endtime - startime))


if __name__ == '__main__':
    #resnet34_UCMerced_main()
    resnet34_cifar_main()
