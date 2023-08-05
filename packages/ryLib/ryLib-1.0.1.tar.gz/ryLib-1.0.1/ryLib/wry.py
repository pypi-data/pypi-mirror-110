#请认准一下红色字体：
#include 王若宇版权所有
import pygame,turtle,time,sys;from sys import stdin,stdout
import math,random
#王若宇库
if __name__ !="__main__":
    print("欢迎使用王若宇库，更多有趣Python请关注编程社区@王若宇")
else:
    print("如果本作品作者不是王若宇，请举报本作品，因为本作品是盗版作品")
    sys.exit()
class info(object):
    #王若宇库的关于模块
    def __init__(*nr):
        print("模块信息：info ，用于显示库信息")
    def edition(*inp):
        return "该库版本为1.01，是最新版本。"
    def by(*inp):
        return "作者为王若宇，本库是正版，可以使用"
class std(info):
    #王若宇库的输入输出模块
    def __init__(self,*oo):
        print("模块信息：输入输出库，用于优化显示输出")
    def printout(*op):
        #输出
        for oution in op:
            for o in oution:
                stdout.write(o)
                stdout.flush()
                time.sleep(0.05)
    def inputf(*io):
        for i in io:
            std.printout(i)
        return stdin.readline()
    def flush(self):
        stdout.flush()
class maths:
    def __init__(self):
        print("模块信息：数学模块，计算数学")
    def add(num):
        printf=0
        for i in num:
            printf+=i
        return printf
    def minus(nmu):
        cout=nmu[0]
        del nmu[0]
        for i in nmu:
            cout-=i
    def randNum(x,y):
        return random.randint(x,y)
    def randLis(lis):
        return random.choice(lis)
    def pai():
        return maths.pi()
class re(maths):
    def __init__(self):
        print("模块信息：re模块，进行文本、列表编辑")
    def replace(Replace="",inText="",to=""):
    #新增：王若宇库re模块
        return inText.replace(Replace,to)
    def deleted(text,range=0):
        del text[range]
        return text
    def convert(a,to="str"):
        if to== "str" or to== "text":
            return str(a)
        elif to== "int" or to== "number":
            return int(a)
        elif to== "float":
            return float(a)
        elif to== "tuple":
            return tuple(a)
        elif to== "list":
            return list(a)
    def split(ap,fengefu= ",",perText=False):
        if perText:
            return list(ap)
        else:
            return ap.split(fengefu)