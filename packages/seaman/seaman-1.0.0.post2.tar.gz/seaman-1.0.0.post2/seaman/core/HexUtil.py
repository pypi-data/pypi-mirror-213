import binascii


# 字符串16进制加密
def encrypt(string: str) -> str:
    """加密字符串，返回加密后的16进制字符串"""
    # 将字符串转换为字节序列
    byte_str = string.encode('utf-8')
    # 将字节序列转换为整数
    num = int.from_bytes(byte_str, byteorder='big')
    # 将整数转换为16进制字符串
    hex_str = hex(num)
    # 去掉字符串开头的'0x'前缀
    hex_str = hex_str[2:]
    return hex_str


def encodeHexStr(_str_: str) -> str:
    return encrypt(_str_)


def encode_hex_str(_str_: str) -> str:
    return encrypt(_str_)


# 字符串16进制解密
def decrypt(hex_str: str) -> str:
    """解密16进制字符串，返回解密后的字符串"""
    # 将16进制字符串转换为整数
    num = int(hex_str, 16)
    # 将整数转换为字节序列
    byte_str = num.to_bytes((num.bit_length() + 7) // 8, byteorder='big')
    # 将字节序列解码为字符串
    string = byte_str.decode('utf-8')
    return string


def decodeHexStr(_str: str) -> str:
    return decrypt(_str)


def decode_hex_str(_str_: str) -> str:
    return decrypt(_str_)


if __name__ == '__main__':
    _str_: str = 'hello,world'
    en_str = encrypt(_str_)
    print(en_str)
    print(decrypt(en_str))
