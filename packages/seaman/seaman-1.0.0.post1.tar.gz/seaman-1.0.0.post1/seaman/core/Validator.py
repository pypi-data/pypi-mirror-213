import re


# 判断值是否为空
def isEmpty(val: object) -> bool:

    if val is None:
        return True
    elif val == '':
        return True
    elif val is []:
        return True
    elif val is {}:
        return True
    return False


def is_empty(val: object) -> bool:
    return isEmpty(val)


# 判断值是否不为空
def isNotEmpty(val: object) -> bool:
    if isEmpty(val):
        return False
    else:
        return True


def is_not_empty(val: object) -> bool:
    return isNotEmpty(val)


# 判断是否为邮箱
def is_email(val: str) -> bool:
    email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return email_regex.match(val) is not None


def isEmail(val: str) -> bool:
    return is_email(val)


def is_mobile(val: str) -> bool:
    phone_regex = re.compile(r'^1[3-9]\d{9}$')
    return phone_regex.match(val) is not None


def isMobile(val: str) -> bool:
    return is_mobile(val)


# 身份证号码匹配
def is_citizen_id(val: str) -> bool:
    id_regex = re.compile(r'^[1-9]\d{5}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[0-1])\d{3}[\dXx]$')
    return id_regex.match(val) is not None


def isCitizenId(val: str) -> bool:
    return is_citizen_id(val)


# 判断字符串是否为数字
def is_number(val: str) -> bool:
    number_regex = re.compile(r'^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$')
    return number_regex.match(val) is not None


def isNumber(val: str) -> bool:
    return is_number(val)


# 判断是否都是汉字
def is_chinese(val: str) -> bool:
    return bool(re.match(r'^[\u4e00-\u9fff]+$', val))


def isChinese(val: str) -> bool:
    return is_chinese(val)


# 判断是否包含汉字
def has_chinese(val: str) -> bool:
    """检查给定的字符串是否包含汉字"""
    return bool(re.search(r'[\u4e00-\u9fff]', val))


def hasChinese(val: str) -> bool:
    return has_chinese(val)


if __name__ == '__main__':
    # print(is_email('1025584691qq@'))
    # print(is_mobile('11689952150'))
    print(is_citizen_id('xxx'))
    print(has_chinese("你好！"))
    #
