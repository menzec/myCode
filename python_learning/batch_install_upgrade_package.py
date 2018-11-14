# -*-coding: utf-8 -*-
import platform
import pip
# pip V10.0.0以上版本需要导入下面的包
from pip._internal.utils.misc import get_installed_distributions
from subprocess import call
from time import sleep
import os
import subprocess

def platform_info():
    # ouput system type and version info
    print("platform.machine()=%s", platform.machine())
    print("platform.node()=%s", platform.node())
    print("platform.platform()=%s", platform.platform())
    print("platform.processor()=%s", platform.processor())
    print("platform.python_build()=%s", platform.python_build())
    print("platform.python_compiler()=%s", platform.python_compiler())
    print("platform.python_branch()=%s", platform.python_branch())
    print("platform.python_implementation()=%s",
          platform.python_implementation())
    print("platform.python_revision()=%s", platform.python_revision())
    print("platform.python_version()=%s", platform.python_version())
    print("platform.python_version_tuple()=%s",
          platform.python_version_tuple())
    print("platform.release()=%s", platform.release())
    print("platform.system()=%s", platform.system())
    #print("platform.system_alias()=%s", platform.system_alias());
    print("platform.version()=%s", platform.version())
    print("platform.uname()=%s", platform.uname())


def pip_upgrade_package():
    print('current platform system is %s' % (platform.system()))
    if str(platform.system()) == 'Windows':
        for dist in get_installed_distributions():
            # 执行后，pip默认为Python3版本
            # 双版本下需要更新Python2版本的包，使用py2运行，并将pip修改成pip2
            #call("sudo pip install --upgrade " + dist.project_name, shell=True)
            os.system("pip install --upgrade " + dist.project_name)
    elif platform.system() == 'Linux':
        for dist in get_installed_distributions():
            os.system("sudo -H pip install --upgrade " + dist.project_name)


def python_install_package(packagefolder):
    print('current platform system is %s' % (platform.system()))
    packagelist = os.listdir(packagefolder)
    i = 0
    tem = len(packagelist)
    num = (tem*tem + tem)/2 + 1
    if str(platform.system()) == 'Windows':
        while len(packagelist):
            if tem != len(packagelist):
                num = (tem*tem + tem)/2 + 1
                tem = len(packagelist)
                i = 0
            if i>num:
                break
            i = i + 1
            package_absdir = packagefolder + '/'+packagelist[0]
            if os.path.isfile(package_absdir):
                if os.system(r'pip install '+package_absdir):
                    print(r'pip install %s failed!'%packagelist[0])
                    packagelist.append(packagelist[0])
                else:
                    print(r'pip install %s successeded!'%packagelist[0])
                del packagelist[0]
                print('len(packagelist): %d'%len(packagelist))
  
                
            # else:
            #     # os.system(packagefolder[0]+':')
            #     print('%s/%s'%(packagefolder,package))
            #     os.chdir(package_absdir)
            #     call(r'cd package_absdirpython')
            #     call('python setup.py install')
    # elif platform.system() == 'Linux':
    #     for dist in get_installed_distributions():
    #         os.system("sudo -H pip install --upgrade " + dist.project_name)


def main():
    # platform_info()
    # pip_upgrade_package()
    python_install_package(r'D:\data\python-software\third_package')


if __name__ == '__main__':
    main()
