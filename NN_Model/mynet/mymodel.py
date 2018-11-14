#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-01 10:03:47
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


class Net_para():
    '''神经网络参数设置'''

    def __init__(self, optimizer,  Epoch, Batch_Size, device,
                 pre_epoch=0, scheduler=None, criterion=nn.CrossEntropyLoss(),
                 ):
        self.epoch = Epoch  # 遍历数据集次数
        self.pre_epoch = pre_epoch  # 定义已经遍历数据集的次数
        self.batch_size = Batch_Size  # 批处理尺寸(batch_size)
        # self.lr = Learning_Rate  # 学习率
        # 定义损失函数和优化方式
        self.criterion = criterion  # 损失函数为交叉熵，多用于多分类问题
        # 优化方式为mini-batch momentum-SGD，并采用L2正则化（权重衰减）
        self.optimizer = optimizer
        self.device = device
        self.scheduler = scheduler

    def get_para(self):
        return [self.epoch, self.pre_epoch, self.batch_size, self.criterion, self.optimizer, self.device, self.scheduler]

    def __repr__(self):
        return ('Para:\n\tAll epoch:%d\n\tBatch size:%d\n\tcriterion:%s\n\toptimizer:%s\n\tdevice: %s\n\tscheduler:%s\n'
                % (self.epoch, self.batch_size, self.criterion, self.optimizer, self.device, self.scheduler))


class mzc_net():

    def __init__(self, wkdir, data, parameters):
        self.traindata, self.testdata = data
        self.para = parameters
        self.wkdir = wkdir

    def get_best_acc(self):
        if os.path.exists(self.wkdir + "/log/best_acc.txt"):
            with open(self.wkdir + "/log/best_acc.txt", 'r') as best_acc_f:
                best_acc_str = best_acc_f.readline()
                best_acc = float(
                    best_acc_str[best_acc_str.rfind('=') + 1:best_acc_str.rfind('%')])
                best_epoch = float(
                    best_acc_str[best_acc_str.find('=') + 1:best_acc_str.find(',')])
        else:
            best_acc = 0.0
            best_epoch = 0
        return (best_epoch, best_acc)

    def pre_check(self, net):
        # if os.path.exists(self.wkdir + '/log/model.txt'):
        #     modelfile = open(self.wkdir + '/log/model.txt', 'w')
        #     print(net, file=modelfile)
        #     modelfile.close()
        # 检查是否存在以前的训练的数据模型,如果存在，加载最新的
        folderlist = ['log', 'model']
        for foldertemp in folderlist:
            if not os.path.exists('%s/%s' % (self.wkdir, foldertemp)):
                os.mkdir('%s/%s' % (self.wkdir, foldertemp))
                print('create folder %s/%s' % (self.wkdir, foldertemp))
        if os.path.exists(self.wkdir + '/model'):
            model_list = os.listdir(self.wkdir + '/model')
            self.para.pre_epoch = len(model_list)
            with open('%s/para.txt' % (self.wkdir), 'a') as parafile:
                parafile.write('pre epoch:%d\n%s' %
                               (self.para.pre_epoch, self.para))
            if self.para.pre_epoch:
                net.load_state_dict(torch.load(
                    self.wkdir + '/model/' + model_list[-1], map_location=self.para.device))
                print('load model %s' % (model_list[-1]))
                for i in range(0, self.para.pre_epoch):
                    self.para.scheduler.step()
                return 0
            else:
                print('model folder has no model file！')
        self.para.pre_epoch = 0

    def train(self, net, epoch, load_best_model=True):
        EPOCH, pre_epoch, BATCH_SIZE, criterion, optimizer, device, scheduler = self.para.get_para()
        lr_befor_step = scheduler.get_lr()
        if lr_befor_step != scheduler.get_lr():
            best_epoch = self.get_best_acc()[0]
            net.load_state_dict(torch.load(
                '%s/model/net_%03d.pth' % (self.wkdir, best_epoch), map_location=self.para.device))
        trainloader = self.traindata
        with open(self.wkdir + '/log/train.txt', 'a') as trainlog:
            torch.no_grad()
            print('Epoch: %d' % (epoch + 1))
            startime = datetime.datetime.now()
            print('startime: %s' % startime)
            net.train()
            sum_loss = 0.0
            correct = 0.0
            total = 0.0
            net = net.to(device)
            for i, data in enumerate(trainloader, 0):
                # 准备数据
                length = len(trainloader)
                inputs, labels = data
                inputs, labels = inputs.to(device), labels.to(device)
                optimizer.zero_grad()
                # forward + backward
                outputs = net(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                # 每训练  个batch打印一次loss和准确率
                sum_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += predicted.eq(labels.data).cpu().sum()
                print('[epoch:%03d, iter:%05d] Loss: %.03f | Acc: %.3f%%'
                      % (epoch + 1, (i + 1 + epoch * length), sum_loss / (i + 1), 100.0 * float(correct) / float(total)), file=trainlog)
                trainlog.flush()
                if (i + 1) % 1 == 0:
                    print('[epoch:%d, iter:%d] Loss: %.03f | Acc: %.3f%%'
                          % (epoch + 1, (i + 1 + epoch * length), sum_loss / (i + 1), 100.0 * float(correct) / float(total)))
                inputs, labels = inputs.to(torch.device(
                    'cpu')), labels.to(torch.device('cpu'))
            net = net.to(torch.device('cpu'))
            torch.cuda.empty_cache()
            endtime = datetime.datetime.now()
            print('endtime: %s |cost time: %s' % (endtime, endtime - startime))
            print('endtime: %s |cost time: %s' %
                  (endtime, endtime - startime), file=trainlog)
            torch.save(net.state_dict(), '%s/model/net_%03d.pth' %
                       (self.wkdir, epoch + 1))
            print('Saving model %s/model/net_%03d.pth' %
                  (self.wkdir, epoch + 1))

    def test(self, net, epoch, classes_label):
        testloader = self.testdata
        device = self.para.device
        print('Testing...%d' % (epoch + 1))
        torch.no_grad()
        correct = 0
        total = 0
        class_acc = [[0, 0] for i in range(len(classes_label))]
        net = net.to(device)
        for data in testloader:
            net.eval()
            images, labels = data
            images, labels = images.to(device), labels.to(device)
            outputs = net(images)
            # 取得分最高的那个类 (outputs.data的索引号)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct_info = (predicted == labels)
            correct += correct_info.sum()
            images, labels = images.to(torch.device(
                'cpu')), labels.to(torch.device('cpu'))
            for i in range(len(labels)):
                class_acc[labels[i]][0] += int(correct_info[i])
                class_acc[labels[i]][1] += 1
        acc = 100.0 * float(correct) / float(total)
        # 将每次测试结果实时写入acc.txt文件中
        with open(self.wkdir + '/log/test.txt', 'a') as testlog:
            testlog.write("EPOCH=%03d,Accuracy= %.3f%%\n" % (epoch + 1, acc))
            for i, cla in enumerate(classes_label):
                testlog.write('   {:<20s}: |correct:{:>5d},sum:{:>5d},acc:{:<7.3%}\n'.format(
                    cla, class_acc[i][0], class_acc[i][1], float(class_acc[i][0]) / float(class_acc[i][1])))
            testlog.flush()
        print('测试分类准确率为：%.3f%%' % (100.0 * float(correct) / float(total)))
        # 记录最佳测试分类准确率并写入best_acc.txt文件中
        best_acc_info = self.get_best_acc()
        if acc > best_acc_info[1]:
            best_acclog = open(self.wkdir + "/log/best_acc.txt", "w")
            best_acclog.write("EPOCH=%d,best_acc= %.3f%%" % (epoch + 1, acc))
            best_acclog.close()
        net = net.to(torch.device('cpu'))
        torch.cuda.empty_cache()
        print("epoch %3d Test Finished" % (epoch + 1))
