# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Date    : 2018-10-17 21:28:33
# # @Author  : ${menzec} (${menzc@outlook.com})
# # @Link    : http://example.org
# # @Version : $Id$

# # import os
# # import multiprocessing

# # def do(n):
# #     name = multiprocessing.current_process().name
# #     print(name,'starting')
# #     print("worker ", n)
# #     return ''

# # if __name__ == '__main__' :
# #     numList = []
# #     for i in range(5) :
# #         p = multiprocessing.Process(target=do, args=(i,))
# #         numList.append(p)
# #         p.start()
# #     p.join()
# #     print("Process end.")
# # import random
# # import string

# # def generate_random_str(randomlength=16):
# #     """
# #     生成一个指定长度的随机字符串，其中
# #     string.digits=0123456789
# #     string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
# #     """
# #     str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
# #     random_str = ''.join(str_list)
# #     return random_str

# # f = generate_random_str(24)
# # print (f)
# #     download_file_dir = r"D:\data\qinghua\downloadfile"
# #     save_dir = r'D:\data\qinghua\img'
# # import threading
# # import time


# # def loop(nloop, nsec):
# #     print('start loop %d at:%s' % (nloop, time.ctime()))
# #     time.sleep(nsec)
# #     print('loop %d done at:%s' % (nloop, time.ctime()))


# # def main():
# #     print('starting at: %s' % (time.ctime()))
# #     threads = []
# #     loops = [2, 4]
# #     nloops = range(len(loops))
# #     for i in nloops:
# #         t = threading.Thread(target=loop, args=(i, loops[i]))
# #         threads.append(t)
# #     for i in nloops:
# #         threads[i].start()
# #     for i in nloops:
# #         threads[i].join()
# #     print('All done at:%s' % (time.ctime()))
# # if __name__ == '__main__':
# #     main()
# import threading
# import time
# loops = [2, 4]


# class Mythread(threading.Thread):
#     """docstring for Mythread"""

#     def __init__(self, func, args, name=''):
#         threading.Thread.__init__(self)
#         self.name = name
#         self.func = func
#         self.args = args

#     def run(self):  # 特殊方法必须写为run
#         self.func(*self.args)


# def loop(nloop, nsec):
#     print('start loop %d at:%s' % (nloop, time.ctime()))
#     time.sleep(nsec)
#     print('loop %d done at:%s' % (nloop, time.ctime()))


# def main():
#     print('start main process:%s' % (time.ctime()))
#     threads = []
#     nloops = range(len(loops))
#     for i in nloops:
#         t = Mythread(loop, (i, loops[i]), loop.__name__)
#         threads.append(t)
#     for i in nloops:
#         threads[i].start()
#     for i in nloops:
#         threads[i].join()
#     print('All done at %s.'%(time.ctime()))
# if __name__ == '__main__':
#     main()
#!/usr/bin/env python
# _*_ coding:utf-8 _*_


# from multiprocessing import Pool
# from multiprocessing.dummy import Pool as ThreadPool
# from multiprocessing import freeze_support
# import time
# import pdb


# def fun_log(func):
#     def inner(*args, **kwargs):
#         starttime = time.time()
#         func(*args, **kwargs)
#         endtime = time.time()
#         cost_time = endtime - starttime
#         print('The function <%s> cost time:<%s>' % (func.__name__, cost_time))
#     return inner


# def test(m):
#     pdb.set_trace()
#     time.sleep(m)
#     return m


# @fun_log
# def MultiProcess(fun, args, n=4):
#     pdb.set_trace()
#     pro_pool = Pool(n)
#     for i in range(3):
#         pro_pool.apply_async(func=fun, args=(i + 2,))
#     pro_pool.close()
#     pro_pool.join()


# @fun_log
# def MultiThreading(fun, args, n=5):
#     thr_pool = ThreadPool(n)
#     result = []
#     for i in range(3):
#         result.append(thr_pool.apply_async(func=fun, args=(i + 2,)))
#     thr_pool.close()
#     thr_pool.join()


# def main():
#     MultiProcess(test, 2, n=4)
#     # MultiThreading(test, 2, n=3)
# if __name__ == '__main__':
#     main()
from multiprocessing import Pool, TimeoutError
import time
import os

def f(x):
    return x*x

if __name__ == '__main__':
    # start 4 worker processes
    with Pool(processes=4) as pool:

        # print "[0, 1, 4,..., 81]"
        print(pool.map(f, range(10)))

        # print same numbers in arbitrary order
        print('imap_unordered')
        for i in pool.imap_unordered(f, range(10)):
            print(i)
        print('end')

        # evaluate "f(20)" asynchronously
        res = pool.apply_async(f, (20,))      # runs in *only* one process
        print(res.get(timeout=1))             # prints "400"

        # evaluate "os.getpid()" asynchronously
        res = pool.apply_async(os.getpid, ()) # runs in *only* one process
        print(res.get(timeout=1))             # prints the PID of that process

        # launching multiple evaluations asynchronously *may* use more processes
        multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
        print([res.get(timeout=1) for res in multiple_results])

        # make a single worker sleep for 10 secs
        res = pool.apply_async(time.sleep, (10,))
        try:
            print(res.get(timeout=1))
        except TimeoutError:
            print("We lacked patience and got a multiprocessing.TimeoutError")

        print("For the moment, the pool remains available for more work")

    # exiting the 'with'-block has stopped the pool
    print("Now the pool is closed and no longer available")