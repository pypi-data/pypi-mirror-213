# 加法哈希
def additiveHash(_str_: str, table_size: int) -> int:
    """
        计算字符串 s 的加法哈希值
        """
    hash_value = 0
    for c in _str_:
        hash_value += ord(c)
    return hash_value % table_size


def additive_hash(_str_: str, table_size: int) -> int:
    return additiveHash(_str_, table_size)


# 旋转哈希
def rotating_hash(s: str, table_size: int) -> int:
    """
    计算字符串 s 的旋转哈希值
    """
    hash_value = 0
    for c in s:
        # 将哈希值左移 1 位，并将当前字符的 ASCII 码值与哈希值相加
        hash_value = (hash_value << 1) + ord(c)
    return hash_value % table_size


def rotatingHash(s: str, table_size: int) -> int:
    return rotating_hash(s, table_size)


if __name__ == '__main__':
    print("hello")
