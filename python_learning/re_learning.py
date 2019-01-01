import re
if __name__ == '__main__':
    a = "123abc456"
    print(re.search("[0-9]*[a-z]*[0-9]*",a).group(0))   #123abc456,返回整体
    print(re.search("[0-9]*[a-z]*[0-9]*",a).span())   #123
    # print(re.search("([0-9]*)([a-z]*)([0-9]*)",a).group(2))   #abc
    # print(re.search("([0-9]*)([a-z]*)([0-9]*)",a).group(3))   #456
    # print(re.search("[0-9]*[a-z]*[0-9]*",a).groups())