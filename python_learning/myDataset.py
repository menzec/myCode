# -*- coding:utf-8 -*-
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


def CheckImage(rootdir, filename_dataset):
    '''This function check whether the images have the right sizes'''
    fn = open(root + filename_dataset, 'r')
    count = 0
    err_size_count = 0
    err_notfound_count = 0
    notcorrect_filename = []
    image_name = fn.readline()
    while image_name:
        image_name = image_name.split(' ', 1)[0]
        if os.path.exists(root + image_name):
            image_data = Image.open(root + image_name)
            if image_data.size[0] != 256 or image_data.size[1] != 256:
                notcorrect_filename.append((image_name, image_data.size))
                err_size_count += 1
        else:
            err_notfound_count += 1
        image_name = fn.readline()
        count += 1
    fn.close()
    notcorrect_filename.append(
        (('image_count', count), ('err_size_count', err_size_count), ('err_notfound_count', err_notfound_count)))
    return notcorrect_filename


#print('build index:', GetImageList(root, 'test01.txt', ['.tif']))
#print('check result:', CheckImageExist(root, 'test01.txt'))


def RemoveBadImage(root, ImageList):
    if root[-1] not in ['\\', '/']:
        root += ('/')
    errImageDir = root + 'errImage\\'
    if not os.path.exists(errImageDir):
        os.mkdir(errImageDir)
    for image_name in ImageList:
        shutil.move(root + image_name, errImageDir)


def divideTrTe(root, rate, file_extension):
    '''将root目录下的影像中的rate比例分为训练集，剩下作为测试集'''
    if root[-1] not in ['\\', '/']:
        root += ('/')
    all_image = GetImageList(root, 'list.txt', file_extension)
    check_result = CheckImage(root, 'list.txt')
    print(check_result[-1])
    errImageList = []
    for name in check_result:
        errImageList.append(name[0])
    errImageList.pop()
    RemoveBadImage(root, errImageList)
    print('delete not qualified image:%-6d' % (len(errImageList)))
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


if __name__ == '__main__':

    root = 'D:\\data\\UCMerced\\training\\'
    file_extension = ['.tif']
    divideTrTe(root, 0.9, file_extension)
