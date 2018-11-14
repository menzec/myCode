from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing
import xlrd
import shutil
import os
import datetime
import pdb

# 查找文件夹和文件类


class Search_files(object):
    """docstring for Search_files"""

    def __init__(self):
        super(Search_files, self).__init__()
        # self.arg = arg

    def search(self, filename, source_dir, files=True, all_files=False):
        dir_file_list = ['dirs', 'files']
        index = 1 if files else 0
        if all_files:
            find_file_list = []
        # pdb.set_trace()
        for fpathe, dir_file_list[0], dir_file_list[1] in os.walk(source_dir):
            if filename in dir_file_list[index]:
                find_file = fpathe + '\\' + filename
                if all_files:
                    find_file_list.append(find_file)
                else:
                    return find_file
        if all_files:
            return find_file_list
        else:
            return ''

    def multi_thread(self):

    def fast_search(self, filenames, thread_num=8, pool_num=multiprocessing.cpu_count() // 2,*args,**kwargs):
        pro_pool = Pool(pool_num)

        for i in range(thread_num):

        pro_num = 0
        while index < len(filenames)
            files_temp = [index:index+thread_num]
            pro_pool.apply_async(func= self.search(),args=(files_temp))
        # thr_pool = ThreadPool(thread_num)
        pro_pool.close()
        pro_pool.join()


def main():
    table = data.sheets()[0]
    nrows = table.nrows
    # 需要复制的文件夹名称列表
    foldername_lists = table.col_values(0)
    data = xlrd.open_workbook(
        r'X:\DATA\1-中间成果\接边参考数据\拷贝脚本-menzecheng\伊朗与土耳其接边--最终提取图幅列表-用于拷贝脚本.xlsx')
    # 源路径
    fromDirList = [r'X:\quanqiu02_2017\2-成果数据省局提供\陕西局\伊朗北部\DSM', ]
    toDir = r'X:\DATA\1-中间成果\接边参考数据\与2018年第二批汇交数据接边\伊朗与土耳其接边\DSM-DDG'
if __name__ == "__main__":
    # fromDirList = r'D:/'
    # testcp = multi_fd_cp()
    # print(testcp.search(filename='log', files = False,source_dir=fromDirList, all_files=1))
