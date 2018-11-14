#-*-coding=utf-8-*-
# import torch
# import inspect

# from torchvision import models

# torch.cuda.empty_cache()
# # 只有执行完上面这句，显存才会在Nvidia-smi中释放

# with torch.no_grad():
# # from gpu_mem_track import MemTracker
# # import os


# def batch_rename(filedir):
#     filenames = os.listdir(filedir)
#     for filename in filenames:
#         os.rename(filedir + '/' + filename,
#                   filedir + '/' + filename.replace('_512.tif', '_1024.tif'))
#     print('done')


# def main():
#     filedir = r'D:\data\airport\download_file0916_1024'
#     batch_rename(filedir)

# if __name__ == '__main__':
#     main()

# import os

# print('Process (%s) start...' % os.getpid())
# # Only works on Unix/Linux/Mac:
# pid = os.fork()
# if pid == 0:
#     print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
# else:
#     print('I (%s) just created a child process (%s).' % (os.getpid(), pid))

# import torch.optim as optim
# import torchvision


# net = torchvision.models.resnet18()
# optimizer = optim.SGD(
#     net.parameters(), lr=0.01, momentum=0.9, weight_decay=5e-4)
# print('id(optimizer): {0:0>15d}'.format(id(optimizer)))
import os
import io

fn = open('download_file0916_1024.pdt')
st = fn.readlines()
print(len(st))
print(io.DEFAULT_BUFFER_SIZE)
