#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-29 15:48:33
# @Author  : ${menzec} (${menzc@outlook.com})
# @Link    : http://example.org
# @Version : $Id$

import torch
import torchvision
from torchvision import transforms, datasets
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import os
import shutil


def GetImageList(root, txtfilename, file_extensions):
    '''将root目录下的对应file_extensions后缀名的文件名汇集在txtfilename文件中，每一类文件的文件名前的英文名称应该一致，仅仅是后面数字不一致,返回一个字典{‘classname’：[label,count]}'''
    if root[-1] not in ['\\', '/']:
        root += ('/')
    categories = [[], [], []]
    str_num = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
    txt_fw = open(root + txtfilename, 'w')
    classes = 0
    for files in os.listdir(root):
        if os.path.isdir(files):
            continue
        elif os.path.splitext(files)[1] in file_extensions:
            filename = os.path.splitext(files)[0]
            i = -1
            while filename[i] >= '0' and filename[i] <= '9':
                i -= 1
            category = filename[:len(filename) + i + 1]
            if not category in categories[0]:
                categories[0].append(category)
                categories[1].append(classes)
                categories[2].append(0)
                classes += 1
            txt_fw.write(
                files + ' ' + str(categories[1][categories[0].index(category)]) + '\n')
            categories[2][categories[0].index(category)] += 1
    txt_fw.close()
    return categories


def CheckImage(root, filename_dataset, rows=256, cols=256):
    '''This function check whether the images have the right sizes'''
    fn = open(root + filename_dataset, 'r')
    count, resize_count, err_size_count, err_notfound_count = 0, 0, 0, 0
    notcorrect_filename = []
    image_name = fn.readline()
    errImageDir = root + '/errImage'
    if not os.path.exists(errImageDir):
        os.mkdir(errImageDir)
    while image_name:
        image_name = image_name.split(' ', 1)[0]
        if os.path.exists(root + image_name):
            image_data = Image.open(root + image_name)
            if image_data.size[0] != rows or image_data.size[1] != cols:
                if abs(rows - image_data.size[0]) < rows * 0.1 or abs(image_data.size[1] != cols) < cols * 0.1:
                    image_data = image_data.resize(
                        (rows, cols), Image.BILINEAR)
                    shutil.move(root + image_name, errImageDir)
                    image_data.save(root + image_name)
                    resize_count += 1
                else:
                    shutil.move(root + image_name, errImageDir)
                    err_size_count += 1
            notcorrect_filename.append((image_name, image_data.size))
        else:
            err_notfound_count += 1
        image_name = fn.readline()
        count += 1
    fn.close()
    notcorrect_filename.append(
        (('image_count', count), ('resize_count: ', resize_count),
         ('err_size_count', err_size_count), ('err_notfound_count', err_notfound_count))
    )
    return notcorrect_filename


def RemoveBadImage(root, ImageList):
    if root[-1] not in ['\\', '/']:
        root += ('/')
    errImageDir = root + 'errImage\\'
    if not os.path.exists(errImageDir):
        os.mkdir(errImageDir)
    for image_name in ImageList:
        shutil.move(root + image_name, errImageDir)


def divideTrTe(root, rate=0.8, file_extension=['.tif', '.jpg', '.bmp']):
    '''将root目录下的影像中的rate比例分为训练集，剩下作为测试集'''
    if root[-1] not in ['\\', '/']:
        root += ('/')
    all_image = GetImageList(root, 'list.txt', file_extension)
    check_result = CheckImage(root, 'list.txt')
    print(check_result[-1])
    # errImageList = []
    # for name in check_result:
    #     errImageList.append(name[0])
    # errImageList.pop()
    # RemoveBadImage(root, errImageList)
    # print('delete not qualified image:%-6d' % (len(errImageList)))
    all_image = GetImageList(root, 'list.txt', file_extension)
    print('image_count:', sum(all_image[2]))
    # 按照比例分为训练集和测试集
    train_fn = open(root + 'train.txt', 'w')
    test_fn = open(root + 'test.txt', 'w')
    list_fn = open(root + 'list.txt', 'r')
    classes = 0
    for category in all_image[0]:
        one_count = all_image[2][all_image[0].index(category)]
        train_count = int(one_count * rate)
        i = 0
        while i < train_count:
            i += 1
            train_fn.write(list_fn.readline())
        while i < one_count:
            i += 1
            test_fn.write(list_fn.readline())
        print('%-18s:%-5d,train count:%-5d,test count %-5d' %
              (category, one_count, train_count, one_count - train_count))
    train_fn.close()
    test_fn.close()
    list_fn.close()


class MyDataset(Dataset):

    def __init__(self, txt, loader, transform=None, target_transform=None):
        fh = open(txt, 'r')
        imgs = []
        for line in fh:
            line = line.strip('\n')
            line = line.rstrip()
            words = line.split()
            imgs.append((words[0], int(words[1])))
        self.imgs = imgs
        self.transform = transform
        self.target_transform = target_transform
        self.loader = loader

    def __getitem__(self, index):
        fn, label = self.imgs[index]
        img = self.loader(fn)
        if self.transform is not None:
            img = self.transform(img)
        return img, label

    def __len__(self):
        return len(self.imgs)


class hymenoptera():

    def __init__(self, root, BATCH_SIZE):
        self.root = root
        self.batch_size = BATCH_SIZE

    def getdata(self, pretrained=True):
        if pretrained == True:
            transform_train = transforms.Compose([
                transforms.RandomResizedCrop(224),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [
                                     0.229, 0.224, 0.225]),
            ])
            transform_test = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [
                                     0.229, 0.224, 0.225]),
            ])
        train_data = datasets.ImageFolder(os.path.join(
            self.root, "train"), transform=transform_train)
        test_data = datasets.ImageFolder(os.path.join(
            self.root, "val"), transform=transform_test)
        train_loader = DataLoader(
            dataset=train_data, batch_size=self.batch_size, shuffle=True, num_workers=2)
        test_loader = DataLoader(
            dataset=test_data, batch_size=self.batch_size, num_workers=2)
        return [train_loader, test_loader]

    @classmethod
    def label(self):
        return ('ants', 'bees')


class myCifar10():
    # 准备数据集并预处理

    def __init__(self, root, BATCH_SIZE):
        self.root = root
        self.batch_size = BATCH_SIZE

    def getdata(self):
        transform_train = transforms.Compose([
            transforms.Resize(40),
            transforms.RandomCrop(32),  # 先四周填充0，在吧图像随机裁剪成32*32
            transforms.RandomHorizontalFlip(p=0.5),  # 图像一半的概率翻转，一半的概率不翻转
            transforms.RandomVerticalFlip(p=0.5),
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465),
                                 (0.2023, 0.1994, 0.2010)),  # R,G,B每层的归一化用到的均值和方差
        ])
        transform_test = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465),
                                 (0.2023, 0.1994, 0.2010)),
        ])
        trainset = torchvision.datasets.CIFAR10(
            self.root, train=True, download=False, transform=transform_train)  # 训练数据集
        trainloader = torch.utils.data.DataLoader(
            trainset, batch_size=self.batch_size, shuffle=True, num_workers=2)  # 生成一个个batch进行批训练，组成batch的时候顺序打乱取
        testset = torchvision.datasets.CIFAR10(
            self.root, train=False, download=False, transform=transform_test)
        testloader = torch.utils.data.DataLoader(
            testset, batch_size=self.batch_size, shuffle=False, num_workers=2)
        return [trainloader, testloader]

    @classmethod
    def label(self):
        return ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')


class UCMerced():

    def __init__(self, root, BATCH_SIZE):
        self.root = root
        self.batch_size = BATCH_SIZE

    def loader(self, image_name):
        return Image.open('%s/%s' % (self.root, image_name))

    def getdata(self, pretrained=False):
        if not os.path.exists(self.root + '/test.txt'):
            divideTrTe(self.root, rate=0.9, file_extension=['.tif'])
        if pretrained:
            transform_train = transforms.Compose([
                transforms.RandomResizedCrop(
                    224, scale=(0.5, 1.0), ratio=(0.75, 1.3)),
                transforms.RandomHorizontalFlip(p=0.5),  # 图像一半的概率翻转，一半的概率不翻转
                transforms.RandomVerticalFlip(p=0.5),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225]),  # R,G,B每层的归一化用到的均值和方差
            ])
            transform_test = transforms.Compose([
                transforms.Resize(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225]),
            ])
        else:
            transform_train = transforms.Compose([
                transforms.RandomResizedCrop(
                    256, scale=(0.5, 1.0), ratio=(0.75, 1.3)),
                # transforms.Resize(280),
                # transforms.RandomCrop(256),  # 先四周填充0，在吧图像随机裁剪成256
                transforms.RandomHorizontalFlip(p=0.5),  # 图像一半的概率翻转，一半的概率不翻转
                transforms.RandomVerticalFlip(p=0.5),
                transforms.ToTensor(),
                transforms.Normalize((0.4842, 0.4901, 0.4505),
                                     (0.2168, 0.2013, 0.1948)),  # R,G,B每层的归一化用到的均值和方差
            ])
            transform_test = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.4842, 0.4901, 0.4505),
                                     (0.2168, 0.2013, 0.1948)),
            ])
        train_data = MyDataset(
            self.root + '/train.txt', self.loader, transform=transform_train)
        test_data = MyDataset(
            self.root + '/test.txt', self.loader, transform=transform_test)
        train_loader = DataLoader(
            dataset=train_data, batch_size=self.batch_size, shuffle=True, num_workers=2)
        test_loader = DataLoader(
            dataset=test_data, batch_size=self.batch_size, num_workers=2)
        return [train_loader, test_loader]

    @classmethod
    def label(self):
        return ('baseballdiamond', 'denseresidential', 'harbor', 'overpass', 'sparseresidential', 'beach', 'forest',
                'intersection', 'parkinglot', 'storagetanks', 'agricultural', 'buildings', 'freeway', 'mediumresidential',
                'river', 'tenniscourt', 'airplane', 'chaparral', 'golfcourse', 'mobilehomepark', 'runway')
