import re


# 字符串截取
def sub(_str_: str, start: int, end: int) -> str:
    # str_len: int = len(_str_)
    if end < start:
        t_str = _str_[end:start]
        return ''.join(reversed(t_str))
    return _str_[start:end]


# 截取最后一个 _str_ _c_ 字符串后的内容
def substringAfterLast(_str_: str, _c_: str) -> str:
    try:
        index = _str_.rindex(_c_)
        return _str_[index + 1:]
    except Exception as e:
        print(e)
        return ''


def sub_string_after_last(_str_: str, _c_: str) -> str:
    return substringAfterLast(_str_, _c_)


# 移除前缀
def remove_prefix(_str_: str, _sub_: str) -> str:
    try:
        index = _str_.index(_sub_)
        return _str_[index + len(_sub_):]
    except Exception as e:
        print(e)
        return _str_


def removePrefix(_str_: str, _sub_: str) -> str:
    return remove_prefix(_str_, _sub_)


# 字符串移除后缀
def remove_suffix(_str_: str, _sub_: str) -> str:
    try:
        index = _str_.rindex(_sub_)
        return _str_[:index]
    except Exception as e:
        print(e)
        return _str_


def removeSuffix(_str_: str, _sub_: str) -> str:
    return remove_suffix(_str_, _sub_)


# 截取第一个 _str_ _c_ 字符串后的内容
def substringAfter(_str_: str, _c_: str) -> str:
    try:
        index = _str_.index(_c_)
        return _str_[index + 1:]
    except Exception as e:
        print(e)
        return ''


def sub_string_after(_str_: str, _c_: str) -> str:
    return substringAfter(_str_, _c_)


# 判断字符串中是否有不可见字符
def has_blank(val: str) -> bool:
    """检查给定的字符串中是否包含不可见字符"""
    return bool(re.search(r'[\x00-\x1F\x7F]', val))


def hasBlank(val: str) -> bool:
    return has_blank(val)


#

if __name__ == '__main__':
    # print(hasBlank("hello world"))
    _str_: str = 'hello.girl.png'
    # print(remove_suffix(_str_, '.png'))
    print(sub(_str_, -1, -3))
