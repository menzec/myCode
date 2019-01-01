import time
'''变态跳台阶python'''


def costtime(func):
    def function(*args, **kwargs):
        starttime = time.time()
        result = func(*args, **kwargs)
        endtime = time.time()
        print('start time:%s\nend time:%s\ncost time:%s' %
              (starttime, endtime, endtime - starttime))
        return result

    return function


class Solution(object):
    def __init__(self):
        self.info = 'class test!'

    def jumpFloorII(self, number):
        # write code here
        num = 0
        if number < 2:
            return 1
        for i in range(1, number + 1):
            num += self.jumpFloorII(number - i)
        return num


@costtime
def multiply(A):

    # write code here
    a_array = np.array(A)
    b_array = np.ones(a_array.size)
    for i in range(0, a_array.size):
        for j in range(0, b_array.size):
            if j != i:
                b_array[i] *= a_array[j]
    return b_array


'''积乘数组'''


def multiply_main():
    if __name__ == "__main__":
        import numpy as np
        A = range(2, 6)
        result = multiply(A)
        print(result)


'''正则表达式匹配'''


@costtime
def match(s, pattern):
    # write code here
    def judge(charA, patter):
        if patter == '.':
            return True
        elif charA == patter:
            return True
        else:
            return False

    index_s = 0
    index = 0
    while index < len(pattern):
        if index + 1 < len(pattern) and pattern[index + 1] == '*':
            while index_s < len(s) and judge(s[index_s], pattern[index]):
                index_s += 1
            tem_pat = pattern[index]
            index += 2
            while pattern[index] == tem_pat:
                index += 1
            continue
        if index_s >= len(s):
            return False
        if not judge(s[index_s], pattern[index]):
            return False
        index += 1
        index_s += 1
    if index_s == len(s) and index == len(pattern):
        return True
    else:
        return False


def match_main():
    result = match("aaabbb", "a*abbb")
    print(result)


# if __name__ == '__main__':
#     match_main()


# @costtime
def jumpFloor(number):
    # write code here
    sum = 0
    if number < 3:
        return number
    sum += jumpFloor(number - 1)
    sum += jumpFloor(number - 2)
    return sum


def othersjumpFloor(number):
    f = 1
    g = 2
    number -= 1
    while (number):
        number -= 1
        tem = g
        g += f
        f = tem
    return f


# @costtime
def manytime():
    starttime = time.time()
    for i in range(1, 50):
        jumpFloor(i)
    endtime = time.time()
    print('start time:%s\nend time:%s\ncost time:%s' % (starttime, endtime,
                                                        endtime - starttime))


if __name__ == "__main__":
    manytime()
