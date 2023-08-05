
from  sys import stdin,stdout;import time as timeModule

def printout(*op,end='\n',flush=True,time=0.05,none=None):
    # 输出
    for oution in op:
        for o in oution:
            stdout.write(o)
            stdout.flush()
            timeModule.sleep(time)
        timeModule.sleep(time*10)
    if none==None:
        stdout.write(end)
    if flush:
        stdout.flush()


def inputf(*io):
    for i in io:
        printout(i)
    return stdin.readline()


def flush():
    stdout.flush()