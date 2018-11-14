#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-17 21:02:51
# @Author  : ${menzec} (${menzc@outlook.com})
# @Link    : http://example.org
# @Version : $Id$


import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import datetime
sys.path.append('..')
sys.path.append('./models')
from Dataset import myDataset
from mynet import mymodel
from models import *

from torch.optim import lr_scheduler
import numpy as np
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
import copy

# 更改学习率
Learning_Rate = 0.001
Batch_Size = 4
All_Epoch = 25
# 可视化模型预测


def hymenoptera():
    startime = datetime.datetime.now()
    model_name = 'transforms learning-hymenoptera'
    print('Start train %s,startime:%s' % (model_name, startime))
    # 定义是否使用GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #device = torch.device("cpu")
    print('device: ', device)
    datadir = r'D:\data\hymenoptera_data'
    modeldir = r'D:\data\Model\hymenoptera'
    # 模型定义-
    model_ft = models.resnet18(pretrained=True).to(device)
    num_ftrs = model_ft.fc.in_features
    model_ft.fc = nn.Linear(num_ftrs, 2)
    model_ft = model_ft.to(device)
    # 超参数设置
    optimizer = optim.SGD(model_ft.parameters(),
                          lr=Learning_Rate, momentum=0.9, weight_decay=5e-4)
    net_para = mymodel.Net_para(
        optimizer, Batch_Size=Batch_Size, Epoch=All_Epoch)
    data = myDataset.hymenoptera(datadir, net_para.batch_size).getdata()
    train_net = mymodel.mzc_net(modeldir, data, net_para)
    train_net.pre_check(model_ft)
    parafile = open('%s/para.txt' % (modeldir), 'a')
    print('para.pre_epoch =%d\nBatch_Size = %d\nLearning_Rate = %f\nAll_Eoch = %d\n' % (
        train_net.para.pre_epoch, Batch_Size, Learning_Rate, All_Epoch), file=parafile)
    parafile.close()
    scheduler = torch.optim.lr_scheduler.StepLR(
        optimizer, 7, gamma=0.1, last_epoch=-1)
    for epoch in range(train_net.para.pre_epoch, train_net.para.epoch):
        scheduler.step()
        train_net.train(model_ft, epoch)
        train_net.test(model_ft, epoch)
    endtime = datetime.datetime.now()
    print('%s Training Finished! Endtime:%s, costtime:%s' %
          (model_name, endtime, endtime - startime))

if __name__ == '__main__':

    # models.resnet18(pretrained=True)
    # models.resnet50(pretrained=True)
    # models.resnet101(pretrained=True)
    # models.resnet152(pretrained=True)
    models.densenet121(pretrained=True)
