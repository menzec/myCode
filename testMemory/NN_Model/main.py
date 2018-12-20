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
ALL_EPOCH = 20


def main():
    # 定义是否使用GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print('device: ', device)
    # 超参数设置
    os.chdir(r'D:\Code\NN_Model')
    print(os.getcwd())
    datadir_list = {
        'cifar10': r'D:\data\cifar10',
        'UCMerced': r'D:\data\UCMerced'
    }
    modelrootdir = r'D:\data\Model\test'
    data_infos = {
        #'cifar10': [len(myDataset.myCifar10.label()), myDataset.myCifar10(datadir_list["cifar10"], BATCH_SIZE).getdata()],
        'UCMerced': [len(myDataset.UCMerced.label()),
                     myDataset.UCMerced(datadir_list["UCMerced"], BATCH_SIZE).getdata(pretrained=True)],
    }
    # 循环组合网络和数据
    for dataname, data_info in data_infos.items():
        num_class, data = data_info
        if dataname == 'cifar10':
            img_size = 32
        elif dataname == 'UCMerced':
            img_size = 256 * 256 // 32
        else:
            print('dataname err!')
        model_list = {
            #'ResNet18': torchvision.models.resnet18(pretrained=True)
            'VGG16': VGG('VGG16', num_classes=num_class, datasize=32),
            # 'ResNet34': ResNet34(num_classes=num_class, datasize=img_size),
            # 'ResNet50': ResNet50(num_classes=num_class, datasize=img_size),
            # 'Alexnet': Alexnet(num_classes=num_class, datasize=img_size),
            # #'GoogLeNet': GoogLeNet(num_classes=num_class, datasize=img_size),
            # 'DenseNet121': densenet_cifar(num_classes=num_class),
        }
        for i, model_info in enumerate(model_list.items()):
            model_name, model = model_info
            print('device: ', device)
            startime = datetime.datetime.now()
            print('%d/%d  Start train %s + %s,startime:%s' %
                  (i + 1, len(model_list), model_name, dataname, startime))
            model_save_dir = modelrootdir + '/' + model_name + '_' + dataname
            if not os.path.exists(model_save_dir):
                os.mkdir(model_save_dir)
            # pretrained model
            # for param in model.parameters():
            #     param.requires_grad = False
            # num_ftrs = model.fc.in_features
            # model.fc = nn.Linear(num_ftrs, num_class)
            net = model.to(device)
            optimizer = optim.SGD(
                net.parameters(), lr=LEARNING_RATE, momentum=0.9, weight_decay=5e-4)
            net_para = mymodel.Net_para(
                optimizer, Epoch=ALL_EPOCH, pre_epoch=0, Batch_Size=BATCH_SIZE)
            train_net = mymodel.mzc_net(model_save_dir, data, net_para)
            train_net.pre_check(net)
            scheduler = torch.optim.lr_scheduler.MultiStepLR(
                optimizer, milestones=[2, 4, 6], gamma=0.2)
            current_lr = 0.0
            with open('%s/para.txt' % (model_save_dir), 'a') as parafile:
                for epoch in range(train_net.para.pre_epoch, train_net.para.epoch):
                    if epoch == train_net.para.pre_epoch:
                        print('para.pre_epoch =%d\nBatch_Size = %d\nLearning_Rate = %f\nAll_Eoch = %d\n' % (
                            train_net.para.pre_epoch, BATCH_SIZE, LEARNING_RATE, ALL_EPOCH), file=parafile)
                    scheduler.step()
                    if train_net.para.pre_epoch !=0:
                        for i in range(0,train_net.para.pre_epoch):
                            scheduler.step()
                    if current_lr != optimizer.param_groups[0]['lr']:
                        current_lr = optimizer.param_groups[0]['lr']
                        print('Epoch %d :optimizer'%(epoch), optimizer, file=parafile)
                    train_net.train(net, epoch)
                    # train_net.test(net, epoch)
            endtime = datetime.datetime.now()
            print('%d/%d  %s + %s Training Finished! Endtime:%s, costtime:%s' %
                  (i + 1, len(model_list), model_name, dataname, endtime,  endtime - startime))
        del model_list

if __name__ == '__main__':
    # torchvision.models.vgg19_bn(pretrained=True)
    # torchvision.models.densenet161(pretrained=True)
    # torchvision.models.inception_v3(pretrained=True)
    main()
