def replace(Replace="", inText="", to=""):
    # 新增：王若宇库re模块
    return inText.replace(Replace, to)


def deleted(text, range=0):
    del text[range]
    return text


def convert(a, to="str"):
    if to == "str" or to == "text":
        return str(a)
    elif to == "int" or to == "number":
        return int(a)
    elif to == "float":
        return float(a)
    elif to == "tuple":
        return tuple(a)
    elif to == "list":
        return list(a)


def split(ap, fengefu=",", perText=False):
    if perText:
        return list(ap)
    else:
        return ap.split(fengefu)