import multiprocessing
import os
import pdb
import shutil
import sys
import time
from copy import deepcopy
from multiprocessing.dummy import Pool as ThreadPool

import xlrd

'''需要设置的参数'''
# 存储需要查找文件名 的 表格
FIND_FILE = r'D:\data\00.xlsx'
# 查找的位置（可以多个位置查找）
fromDirList = [r'D:/', r'E:/', r'F:/']
# 是否要查找 目录下所有文件
ALL_FILES = False  # 如果查找所有同名文件(夹)设置为 True ，否则 False
# 将找到的文件目录 拷贝到该目录
# ---最终的拷贝结果-如果Excel中有多个相同的文件名，拷贝目录的文件名后会有多个_1
# ---如果一次找到多个目录，会以（1）、（2）形式递增，第一个没有（）
toDir = r'D:/data/test'
# 每个进程的线程数--个人实验发现多进程下，多线程 并 没 有 什 么 用
THREAD_NUM = 2
# 总进程数 （默认为cpu核数的一半）
POR_NUM = multiprocessing.cpu_count() // 2 + 1


class Search_files(object):
    """查找文件夹和文件类"""

    def __init__(self):
        super(Search_files, self).__init__()

    def search(self, filename, source_dirs, all_files=False):
        '''查找单个文件的函数
        filename 为要查找的文件名
        source_dirs 查找的位置（可以多个位置查找）
        all_files 如果查找所有同名文件(夹)设置为 True ，否则 False'''
        try:
            if all_files:
                find_file_list = []
            for soru_dir in source_dirs:
                for fpathe, dirs, fs in os.walk(soru_dir):
                    if filename in dirs or filename in fs:
                        find_file = fpathe + '\\' + filename
                        if all_files:
                            find_file_list.append(find_file)
                        else:
                            return [find_file]
        except Exception as ex:
            if all_files:
                return find_file_list
            else:
                return ''

    def multi_thread_search(self,
                            queue,
                            thread_num=8,
                            filenames='',
                            *args,
                            **kwargs):
        '''多进程查找
        thread_num 进程数
        *args， **kwargs 为search 函数的参数对 ---建议使用kwargs将参数以字典形式传递过来'''
        try:
            index = 0
            thr_pool = ThreadPool(thread_num)
            # 删除字典 kwargs 中的关键字
            # filenames,这样kwargs能传递给search函数(search函数不接受关键字filenames)
            # filenames = kwargs.pop('filenames')
            result = []

            while index < len(filenames):
                kwargs['filename'] = filenames[index]
                # 线程执行结果为一个对象，get()函数可以获得 该线程执行的函数的 函数返回值
                find_result = thr_pool.apply_async(
                    func=self.search,
                    kwds=deepcopy(kwargs))  #args=(filenames[index],),
                result.append([filenames[index], find_result])
                index += 1
        except Exception as ex:
            print("Error:%s" % (ex))
            sys.stdout.flush()
        thr_pool.close()
        thr_pool.join()
        for res in result:
            queue.put([res[0], res[1].get()])
        # return result

    def fast_search(self,
                    filenames,
                    target,
                    por_num=multiprocessing.cpu_count() // 2,
                    *args,
                    **kwargs):
        '''多进程，多线程查找
        filenames 为要查找的所有文件名，列表格式
        target 为对查找到的文件进行的处理，对该函数传入的参数为--存放结果的队列,总的文件数量--
        和--当前进程处理到第几个文件--
        # 总进程数 （默认为cpu核数的一半）
        *args， **kwargs 为search 函数的参数对 ---建议使用kwargs将参数以字典形式传递过来'''
        try:
            index = 0
            queue = multiprocessing.Manager().Queue()
            # queue = multiprocessing.Queue()
            pro_pool = multiprocessing.Pool(por_num)
            # 针对查找结果 进行自定义的下一步处理
            pro_pool.apply_async(func=target, args=(queue, len(filenames)))
            time.sleep(0.00001)
            thread_num = kwargs.pop('thread_num')
            while index < len(filenames):
                # 按照线程数 给每个进程分配 要查找的文件（数量 = 每个进程的线程数量）
                if index + thread_num < len(filenames):
                    kwargs['filenames'] = filenames[index:index + thread_num]
                else:
                    kwargs['filenames'] = filenames[index:]
                # 线程执行结果为一个对象，get()函数可以获得 该线程执行的函数的 函数返回值
                result = pro_pool.apply_async(
                    func=self.multi_thread_search,
                    args=(queue, thread_num),
                    kwds=deepcopy(kwargs))
                # 如果不休眠则会 报错----原因未知
                time.sleep(0.00001)
                index += thread_num
        except Exception as ex:
            print("Error:%s" % (ex))
            sys.stdout.flush()
            sys.exit()
        pro_pool.close()
        pro_pool.join()


def copy_files(copyfiles):
    '''执行 拷贝的函数'''

    def checkfile_exists(filename):
        '''检查文件是否存在
        如果存在，则新拷贝的文件(夹)后加 _1 '''
        '''日志文件存放在拷贝目录下，名称为copy-log.txt'''
        if os.path.exists(filename):
            if os.path.isfile(filename):
                file_base_name, ext = os.path.splitext(filename)
                new_target = file_base_name + '_1' + ext
                return checkfile_exists(new_target)
            else:
                return checkfile_exists(filename + '_1')
        else:
            return filename

    try:
        target_file = toDir + '/' + copyfiles[0]
        target_file = checkfile_exists(target_file)
        index = 0
        '''如果一个名称找到多个位置,将会以(1)、(2)的形式将文件拷贝过来
        （1）代表的是找到的第二个'''
        for file in copyfiles[1]:
            '''判断是否有多个结果'''
            if index > 0:
                if os.path.isfile(target_file):
                    file_base_name, ext = os.path.splitext(target_file)
                    target_file = file_base_name + \
                        '(' + str(index) + ')' + ext
                else:
                    target_file = target_file + '(' + str(index) + ')'
            '''文件文件夹采用不同的拷贝函数'''
            if os.path.isfile(file):
                shutil.copy2(file, target_file)
            else:
                shutil.copytree(file, target_file)
            index += 1
    except Exception as ex:
        print("Error:%s" % (ex))


def myfun(queue, all_num):
    i = 0
    try:
        with open('%s/copy-log.txt' % (toDir), 'w') as log:
            while os.getppid() and i < all_num:
                if queue.empty():
                    time.sleep(0.5)
                else:
                    i += 1
                    result = queue.get()
                    if len(result[1]):
                        copy_files(result)
                        print('%d-%d-' % (i, all_num), result, file=log)
                        sys.stdout.write(
                            '%d-%d-%s finish!\n' % (i, all_num, result[0]))
                    else:
                        print(
                            '%d-%d-%s-not found' % (i, all_num, result[0]),
                            file=log)
                        sys.stdout.write('%d-%d not found\n' % (i, all_num),
                                         result)
                    log.flush()
                    sys.stdout.flush()
    except Exception as ex:
        print("Error:%s" % (ex))


def read_data():
    '''读取表格信息'''
    data = xlrd.open_workbook(FIND_FILE)
    table = data.sheets()[0]
    filenames = table.col_values(0)
    return filenames


def main():
    filenames = read_data()
    print('start time:%s' % (time.time()))
    testcp = Search_files()
    # testcp.multi_thread_search(
    # thread_num=THREAD_NUM, filenames=filenames, source_dirs=fromDirList,
    # all_files=ALL_FILES)
    testcp.fast_search(
        target=myfun,
        filenames=filenames,
        thread_num=THREAD_NUM,
        por_num=POR_NUM,
        source_dirs=fromDirList,
        all_files=ALL_FILES)
    print('end time:%s' % (time.time()))


def print_cpu_info():
    import platform
    import wmi
    print("您的CPU生产商为:" + platform.machine())
    print("您的CPU家族为:" + platform.processor())
    cpuinfo = wmi.WMI()
    for cpu in cpuinfo.Win32_Processor():
        print("您的CPU序列号为:" + cpu.ProcessorId.strip())
        print("您的CPU名称为:" + cpu.Name)
        print("您的CPU已使用:%d%%" % cpu.LoadPercentage)
        print("您的CPU核心数为:%d" % cpu.NumberOfCores)
        print("您的CPU时钟频率为:%d" % cpu.MaxClockSpeed)


if __name__ == "__main__":
    print_cpu_info()
