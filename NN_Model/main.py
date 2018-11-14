#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-02 13:59:22
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
import pdb
sys.path.append('..')
sys.path.append('./models')
from Dataset import myDataset
from mynet import mymodel
from models import *

# 数据dict={dataname:[num_classes,[traindataloader.testdataloader]]}
# data_infos = {#  myDataset0825.py
#     'cifar10': [len(myDataset.myCifar10.label()), myDataset.myCifar10(datadir_list[0], BATCH_SIZE).getdata()],
#     'myCifar10_normalize': [len(myDataset.myCifar10.label()), myDataset.myCifar10_normalize(datadir_list[0], BATCH_SIZE).getdata()],
#     'myCifar10_train_normalize': [len(myDataset.myCifar10.label()), myDataset.myCifar10_train_normalize(datadir_list[0], BATCH_SIZE).getdata()],
#     'myCifar10_RandomCrop': [len(myDataset.myCifar10.label()), myDataset.myCifar10_RandomCrop(datadir_list[0], BATCH_SIZE).getdata()],
#     'myCifar10_horizonflip': [len(myDataset.myCifar10.label()), myDataset.myCifar10_horizonflip(datadir_list[0], BATCH_SIZE).getdata()],
#     'myCifar10_horizonflip_RandomCrop': [len(myDataset.myCifar10.label()), myDataset.myCifar10_horizonflip_RandomCrop(datadir_list[0], BATCH_SIZE).getdata()],
#     'myCifar10_horizonflip_Normalize': [len(myDataset.myCifar10.label()), myDataset.myCifar10_horizonflip_Normalize(datadir_list[0], BATCH_SIZE).getdata()],
#     'myCifar10_RandomCrop_Normalize': [len(myDataset.myCifar10.label()), myDataset.myCifar10_RandomCrop_Normalize(datadir_list[0], BATCH_SIZE).getdata()],
#     'myCifar10_All': [len(myDataset.myCifar10.label()), myDataset.myCifar10_All(datadir_list['cifar'], BATCH_SIZE).getdata()]
# }

BATCH_SIZE = 64
LEARNING_RATE = 0.02
ALL_EPOCH = 8
MILESTONES = [2,4,6]
MODELDIR = r'D:\data\Model\ResNet50_UCMerced\net_003.pth'
GAMMA = 0.2


def main():
    # 定义是否使用GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print('device: ', device)
    print(os.getcwd())
    datadir_list = {
        'cifar10': r'D:\data\cifar10',
        'UCMerced': r'D:\data\UCMerced'
    }
    modelrootdir = r'D:\data\Model\test'
    data_infos = {
        #'cifar10': [len(myDataset.myCifar10.label()), myDataset.myCifar10(datadir_list["cifar10"], BATCH_SIZE).getdata()],
        'UCMerced': [myDataset.UCMerced.label(),
                     myDataset.UCMerced(datadir_list["UCMerced"], BATCH_SIZE).getdata(pretrained=True)],
    }
    # 循环组合网络和数据
    for dataname, data_info in data_infos.items():
        classes_label, data = data_info
        if dataname == 'cifar10':
            img_size = 32
        elif dataname == 'UCMerced':
            img_size = 256 * 256 // 32
        else:
            print('dataname err!')
        model_list = {
            'ResNet50': torchvision.models.resnet50(pretrained=False)
        }
        for i, model_info in enumerate(model_list.items()):
            model_name, net = model_info
            print('device: ', device)
            startime = datetime.datetime.now()
            print('%d/%d  Start train %s + %s,startime:%s' %
                  (i + 1, len(model_list), model_name, dataname, startime))
            model_save_dir = modelrootdir + '/' + model_name + '_' + dataname
            if not os.path.exists(model_save_dir):
                os.mkdir(model_save_dir)
            # pretrained model
            # for param in net.parameters():
            #     param.requires_grad = False
            num_ftrs = net.fc.in_features
            net.fc = nn.Linear(num_ftrs, len(classes_label))
            net.load_state_dict(torch.load(MODELDIR,map_location=device))
            # optimizer = optim.SGD(
            # net.parameters(), lr=LEARNING_RATE, momentum=0.9,
            # weight_decay=5e-4)
            optimizer = optim.Adam(net.parameters(),
                                   lr=LEARNING_RATE)
            scheduler = torch.optim.lr_scheduler.MultiStepLR(
                optimizer, milestones=MILESTONES, gamma=GAMMA)
            net_para = mymodel.Net_para(
                optimizer, Epoch=ALL_EPOCH, pre_epoch=0, device=device, Batch_Size=BATCH_SIZE, scheduler=scheduler)
            train_net = mymodel.mzc_net(model_save_dir, data, net_para)
            train_net.pre_check(net)
            for epoch in range(train_net.para.pre_epoch, train_net.para.epoch):
                train_net.train(net, epoch)
                train_net.test(net, epoch,classes_label)
            endtime = datetime.datetime.now()
            print('%d/%d  %s + %s Training Finished! Endtime:%s, costtime:%s' %
                  (i + 1, len(model_list), model_name, dataname, endtime,  endtime - startime))
        del model_list

if __name__ == '__main__':
    main()
