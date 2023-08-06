import urllib.parse


# 请求地址编码
def encode(_url_: str) -> str:
    encoded_url = urllib.parse.quote(_url_, safe=':/?&=')
    return encoded_url


# 编码后地址解码
def decode(_str_: str) -> str:
    return urllib.parse.unquote(_str_)


if __name__ == '__main__':
    _url_ = 'https://www.baidu.com?str=你好中国'
    en_str = encode(_url_)
    print(en_str)
    de_str = decode(en_str)
    print(de_str)

