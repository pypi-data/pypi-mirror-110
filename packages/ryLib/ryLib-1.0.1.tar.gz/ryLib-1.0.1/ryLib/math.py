

def add(num):
    printf = 0
    for i in num:
        printf += i
    return printf


def minus(nmu):
    cout = nmu[0]
    del nmu[0]
    for i in nmu:
        cout -= i


def randNum(x, y):
    return random.randint(x, y)


def randLis(lis):
    return random.choice(lis)


def pai():
    return maths.pi()