import xlrd
import shutil
import os
import datetime
data=xlrd.open_workbook(r'D:\data\00.xlsx')
table=data.sheets()[0]
nrows=table.nrows

#需要复制的文件夹名称列表
foldername_lists=table.col_values(0)

#源路径
fromDirList=[r'D:/', ]
toDir =r'D:/data/test'

#查找文件夹函数
def search_copy_folder(foldername, source_dir):
    for fpathe, dirs, fs in os.walk(source_dir):
        ## dirs代表查找的是文件夹，fs代表查找的是文件
        if foldername in fs:
            foler_path=fpathe + '\\'+foldername
            return foler_path
    return ''

if __name__=="__main__":
    i = 1
    logfile = r'copylog.txt'
    with open(logfile,'w') as logfn:
        for folder in foldername_lists:
            starttime = datetime.datetime.now()
            print('\nSearch %s ... start time:%s '%(folder,starttime))
            ## 循环遍历源路径列表的每个文件夹
            for fromDir in fromDirList:
                foler_path=search_copy_folder(folder,fromDir)
##                print('from list',fromDir)
                if foler_path=='':
                    continue
                else:
                    print(folder+"：存在,开始复制")
                    ## 拷贝文件夹
##                    folder_copypath = toDir+'/'+folder
##                    shutil.copytree(foler_path,folder_copypath)
                    ## 拷贝结束
                    ## 拷贝文件
                    folder_copypath = toDir + '/'+folder
                    shutil.copyfile(foler_path,folder_copypath)
                    ## 拷贝结束
                    endtime = datetime.datetime.now()
                    logfn.write('%d,%s copy to %s,cost time:%s\n'
                          %(i,foler_path,folder_copypath,endtime-starttime))
                    print('%d,%s copy to %s,cost time:%s'
                          %(i,foler_path,folder_copypath,endtime-starttime))
                    i += 1
                    break
            if foler_path == '':
                print("'%d,%s 不存在,跳过"%(i,folder))

	




