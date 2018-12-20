'''
ubuntu 安装anaconda后，其路径添加进系统目录，导致系统默认Python为anaconda的python3
将anaconda的python重命名为python3后，/anaconda/bin/目录下的许多扩展包报错，
因为其默认解释器为 /anaconda/bin/python,

此脚本为批量修改anaconda/bin/ 下解释器为/anaconda/bin/python3
'''
import os
import chardet
import shutil


def main():
    rootdir = '/home/men/anaconda3/bin/'
    filenames = os.listdir(rootdir)
    for filename in filenames:
        filepath = rootdir + filename
        fixfile(filepath)


# 二进制读写文件，检测文件是否为ascii码文件
def fixfile(filename):
    temname = '/home/men/test.txt'
    interprestring = b'#!/home/men/anaconda3/bin/python\n'
    fr = open(filename, mode='rb')
    subcontent = fr.read(200)
    result = chardet.detect(subcontent)
    if result['encoding'] == 'ascii' and subcontent[:len(interprestring
                                                         )] == interprestring:
        with open(temname, 'wb') as fw:
            fw.write(b'#!/home/men/anaconda3/bin/python3\n')
            fw.write(subcontent[len(interprestring):])
            fw.write(fr.read())
            fr.close()
            shutil.move(temname, filename)
            print(filename)


if __name__ == '__main__':
    main()