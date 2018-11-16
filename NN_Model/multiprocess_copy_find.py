from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing
import xlrd
import shutil
import os
import time
import pdb

'''需要设置的参数'''
# 存储需要查找文件名 的 表格
FIND_FILE = r'D:\data\00.xlsx'
# 查找的位置（可以多个位置查找）
fromDirList = [r'D:/', ]
# 是否要查找 目录下所有文件
ALL_FILES = True  # 如果查找所有同名文件(夹)设置为 True ，否则 False
# 将找到的文件目录 拷贝到该目录
toDir = 'D:/data/test'
# 每个进程的线程数
THREAD_NUM = 4
# 总进程数 （默认为cpu核数的一半）
POR_NUM = multiprocessing.cpu_count() // 2


class Search_files(object):
    """查找文件夹和文件类"""

    def __init__(self):
        super(Search_files, self).__init__()

    def search(self, filename, source_dirs, all_files=False):
        '''查找单个文件的函数
        filename 为要查找的文件名
        source_dirs 查找的位置（可以多个位置查找）
        all_files 如果查找所有同名文件(夹)设置为 True ，否则 False'''
        if all_files:
            find_file_list = []
        for soru_dir in source_dirs:
            for fpathe, dirs, fs in os.walk(soru_dir):
                if filename in dirs or filename in fs:
                    find_file = fpathe + '\\' + filename
                    if all_files:
                        find_file_list.append(find_file)
                    else:
                        return find_file
        if all_files:
            return find_file_list
        else:
            return ''

    def multi_thread_search(self, thread_num=8, *args, **kwargs):
        '''多进程查找
        thread_num 进程数
        *args， **kwargs 为search 函数的参数对 ---建议使用kwargs将参数以字典形式传递过来'''
        index = 0
        thr_pool = ThreadPool(thread_num)
        # 删除字典 kwargs 中的关键字 filenames,这样kwargs能传递给search函数(search函数不接受关键字filenames)
        filenames = kwargs.pop('filenames')
        result = []
        try:
            while index < len(filenames):
                # 将需要查找的文件名通过kwargs参数传递给search函数
                kwargs['filename'] = filenames[index]
                # 线程执行结果为一个对象，get()函数可以获得 该线程执行的函数的 函数返回值
                find_result = thr_pool.apply_async(
                    func=self.search, args=args, kwds=kwargs)
                result.append([filenames[index], find_result.get()])
                index += 1
        except Exception as ex:
            msg = "Error:%s" % (ex)
            print(msg)
        thr_pool.close()
        thr_pool.join()
        return result

    def fast_search(self, filenames, target, por_num=multiprocessing.cpu_count() // 2, *args, **kwargs):
        '''多进程，多线程查找
        filenames 为要查找的所有文件名，列表格式
        target 为对查找到的文件进行的处理，对该函数传入的参数为--总的文件数量--
        和--当前进程处理到第几个文件--
        # 总进程数 （默认为cpu核数的一半）
        *args， **kwargs 为search 函数的参数对 ---建议使用kwargs将参数以字典形式传递过来'''
        index = 0
        manager = multiprocessing.Manager()
        queue = manager.Queue()
        pro_pool = multiprocessing.Pool(por_num)
        thread_num = kwargs['thread_num']
        try:
            while index < len(filenames):
                # 按照线程数 给每个进程分配 要查找的文件（数量 = 每个进程的线程数量）
                if index + thread_num < len(filenames):
                    kwargs['filenames'] = filenames[index:index + thread_num]
                else:
                    kwargs['filenames'] = filenames[index:]
                # 线程执行结果为一个对象，get()函数可以获得 该线程执行的函数的 函数返回值
                result = pro_pool.apply_async(
                    func=self.multi_thread_search, kwds=kwargs).get()
                # 如果不休眠则会 报错----原因未知
                time.sleep(0.001)
                # 针对查找结果 进行自定义的下一步处理
                pro_pool.apply_async(func=target, args=(
                    result, index, len(filenames)))
                time.sleep(0.001)
                index += thread_num
        except Exception as ex:
            msg = "Error:%s" % (ex)
            print(msg)
        pro_pool.close()
        pro_pool.join()


def copy_files(files, cur_num, all_num):
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
        with open('%s/copy-log.txt' % (toDir), 'w') as log:
            for fileinfo in files:
                print('%s:' % (fileinfo[0]), fileinfo[1], file=log)
        for copyfiles in files:
            target_file = toDir + '/' + copyfiles[0]
            target_file = checkfile_exists(target_file)
            index = 0
            '''如果一个名称找到多个位置,将会以(1)、(2)的形式将文件拷贝过来
            （1）代表的是找到的第二个'''
            for file in copyfiles[1]:
                '''判断找到的结果是否有多个'''
                if index > 0:
                    if os.path.isfile(file):
                        file_base_name, ext = os.path.splitext(file)
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
            cur_num += 1
            '''判断找到的结果是否为空'''
            if len(copyfiles[1]):
                print('%d of %d - %s is finished!' %
                      (cur_num, all_num, copyfiles[0]))
            else:
                print('%d of %d - %s not founds' %
                      (cur_num, all_num, copyfiles[0]))
    except Exception as ex:
        msg = "Error:%s" % (ex)
        print(msg)


def myfun(files, cur_num, all_num):
    copy_files(files, cur_num, all_num)


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
    testcp.fast_search(target=myfun, filenames=filenames,
                       thread_num=THREAD_NUM, por_num=POR_NUM,
                       source_dirs=fromDirList, all_files=ALL_FILES)
    print('end time:%s' % (time.time()))

if __name__ == "__main__":
    main()
