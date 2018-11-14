# -*- coding: utf-8 -*-
# @Date    : 2018-09-06 10:03:26
# @Author  : ${menzec} (${menzc@outlook.com})
# @Link    : http://example.org
# @Version : $Id$

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize


def read_acc(filename):
    with open(filename, 'r') as acc_fn:
        acc_data = acc_fn.readlines()
        result = []
        for i, line in enumerate(acc_data, 0):
            epoch = int(line[line.index('=') + 1:line.index(',')])
            if epoch < len(result):
                del result[epoch - 1:]
            acc = float(line[line.rindex('=') + 1:line.rindex('%')])
            result.append([epoch, acc])
    return result


def read_best_acc(filename):
    with open(filename, 'r') as acc_fn:
        line = acc_fn.readline()
        epoch = int(line[line.index('=') + 1:line.index(',')])
        best_acc = float(line[line.rindex('=') + 1:line.rindex('%')])
    return [epoch, best_acc]


def read_loss(filename):
    with open(filename, 'r') as loss_fn:
        loss_data = loss_fn.readlines()
        result = []
        epoch_loss = []
        for i, line in enumerate(loss_data, 0):
            if line.find('epoch') == -1:
                continue
            cur_epoch = int(line[line.find(':') + 1:line.find(',')])
            if len(result) and cur_epoch < result[-1][0]:
                print('delete %s epoch[%d:],cur_epoch:%d' %
                      (filename, -(result[-1][0] - cur_epoch + 1), cur_epoch))
                del result[-(result[-1][0] - cur_epoch + 1):]
            if i and cur_epoch != last_epoch:
                loss_mean = float(sum(epoch_loss) / len(epoch_loss))
                result.append((last_epoch, loss_mean))
                del epoch_loss
                epoch_loss = []
            cur_iter_num = int(line[line.find('iter:') + 5:line.find('] ')])
            if len(epoch_loss) and last_iter_num >= cur_iter_num:
                print('delete %s epoch %d  iter[%d:],cur_iter_num:%d' % (
                    filename, cur_epoch, -(last_iter_num - cur_iter_num + 1), cur_iter_num))
                del epoch_loss[-(last_iter_num - cur_iter_num + 1):]
            loss = float(line[line.rfind('Loss: ') + 6:line.rfind(' | Acc')])
            epoch_loss.append(loss)
            last_iter_num = cur_iter_num
            last_epoch = cur_epoch
        result.append((last_epoch, float(sum(epoch_loss) / len(epoch_loss))))
    return result


def plot_acc(filedir):
    net_class = os.listdir(filedir)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    for net in net_class:
        if os.path.isfile(filedir + '/' + net):
            continue
        # if net.split('_', 2)[0] != 'DenseNet121':
        #     continue
        testfile = filedir + '/' + net + '/test.txt'
        best_acc_fn = filedir + '/' + net + '/best_acc.txt'
        best_result = read_best_acc(best_acc_fn)
        acc_result = read_acc(testfile)
        acc_array = np.array(acc_result)
        net = net.replace('my', '')
        plt.plot(acc_array[:, 0], acc_array[:, 1], label=net)
        plt.scatter(best_result[0], best_result[1], linewidths=5)
    plt.xlabel('训练次数')
    plt.ylabel('准确率')
    plt.title('Accuracy')
    plt.legend()
    plt.grid(True, linestyle="-", linewidth="1")
    plt.show()


def plot_loss(filedir):
    net_class = os.listdir(filedir)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    for net in net_class:
        if os.path.isfile(filedir + '/' + net):
            continue
        # if net.split('_', 2)[0] != 'DenseNet121':
        #     continue
        testfile = filedir + '/' + net + '/train.txt'
        acc_result = read_loss(testfile)
        acc_array = np.array(acc_result)
        net = net.replace('my', '')
        plt.plot(acc_array[:, 0], acc_array[:, 1], label=net)
    plt.xlabel('迭代次数')
    plt.ylabel('损失值')
    plt.title('损失变化')
    plt.legend()
    plt.grid(True, linestyle="-", linewidth="1")
    plt.show()


def plot_loss_acc(filedir):
    net_class = os.listdir(filedir)
    start_epoch = 0
    plt.rcParams['font.sans-serif'] = ['SimHei']
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    for net in net_class:
        if os.path.isfile(filedir + '/' + net):
            continue
        # if net.split('_', 2)[0] != 'DenseNet121':
        #     continue
        trainfile = filedir + '/' + net + '/train.txt'
        train_result = read_loss(trainfile)
        acc_array = np.array(train_result)
        ax2.plot(acc_array[start_epoch:, 0], acc_array[start_epoch:, 1],
                 label=net.replace('my', '') + '--loss')
        testfile = filedir + '/' + net + '/test.txt'
        best_acc_fn = filedir + '/' + net + '/best_acc.txt'
        best_result = read_best_acc(best_acc_fn)
        acc_result = read_acc(testfile)
        acc_array = np.array(acc_result)
        ax.plot(acc_array[start_epoch:, 0], acc_array[start_epoch:, 1],
                label=net.replace('my', '') + '--acc')
        ax.scatter(best_result[0], best_result[1], linewidths=5)
    ax.set_xlabel('迭代次数')
    ax2.set_ylabel('损失值')
    ax.set_ylabel('准确率')
    ax.set_title('准确率和损失变化')
    ax.legend(loc=2, bbox_to_anchor=(0.6, 0.5), borderaxespad=0.)
    ax2.legend(loc=1, bbox_to_anchor=(0.6, 0.5), borderaxespad=0.)
    ax.grid(True, linestyle="-", linewidth="1")
    plt.show()

# def liner(x, A, B):
#     return A * x + B


# def quadratic_curve(x, A, B, C):
#     return A * x * x + B * x + C

def plot_curve(trainfile):
    train_result = read_loss(trainfile)
    loss_array = np.array(train_result)
    origin_x, origin_y = loss_array[22:150, 0], loss_array[22:150, 1]
    x = np.linspace(origin_x[0], origin_x[-1], loss_array.shape[0] * 3)
    quadratic_curve = np.polyfit(origin_x, origin_y, 2)
    min_curve_loss = -(quadratic_curve[1] / 2 / quadratic_curve[0])
    q1 = np.poly1d(quadratic_curve)
    yvals = q1(x)
    # plot0 = plt.plot(loss_array[:,0],loss_array[:,1])
    plot1 = plt.plot(origin_x, origin_y, 'r', label='original values')
    plot2 = plt.plot(x, yvals, 'g', label='polyfit values')
    print(np.min(loss_array[:, 1]))
    min_loss_all_index = np.where(loss_array[:, 1]==np.min(loss_array[:, 1]))
    min_loss_subx_index = np.where(origin_x==np.min(origin_x))
    print(min_loss_all_index)
    print('curve min loss:{0}\n min loss({1},{2}),sub loss:({3},{4})'.format(min_curve_loss, origin_x[min_loss_subx_index], origin_x[min_loss_subx_index],
                                     loss_array[min_loss_all_index][0], loss_array[min_loss_all_index][1]))
    plt.show()


def main():
    datadir = r'D:\NGCC\deep_learning\workspace'
    plot_loss_acc(datadir)
    # plot_curve(
    #     r'D:\NGCC\deep_learning\workspace\ResNet101-01_nograd_UCMerced\train.txt')

if __name__ == '__main__':
    main()
