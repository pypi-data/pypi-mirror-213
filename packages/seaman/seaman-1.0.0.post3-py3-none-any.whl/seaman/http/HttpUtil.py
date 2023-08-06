import os

import requests
from seaman.core import OsUtil, Validator, StrUtil, UrlUtil


# 请求头常量
class Header:
    CONTENT_TYPE = 'Content-Type'
    SERVER = 'Server'
    CONTENT_DISPOSITION = 'Content-Disposition'


# 字符串编码类型
class Encode:
    ISO_8859_1 = 'ISO_8859_1'
    UTF_8 = 'utf-8'
    GBK = 'gbk'


# mock get 请求
def get(_url_: str) -> requests.Response:
    r = requests.get(_url_)
    return r


# 下载文件 -- 基础版本
def download(_url_: str, _path_: str, _encode_: str = "") -> str:
    # 如果不存在 创建对应目录
    OsUtil.mkdir(_path_)
    r = get(_url_)
    headers = r.headers
    ct_type = headers[Header.CONTENT_TYPE]
    ct_dis = headers[Header.CONTENT_DISPOSITION]
    if Validator.isNotEmpty(_encode_):
        ct_type = ct_type.encode(_encode_)
        ct_dis = ct_dis.encode(_encode_)
        ct_type = ct_type.decode(Encode.UTF_8)
        ct_dis = ct_dis.decode(Encode.UTF_8)

    # print(ct_type)
    # print(ct_dis)
    f_name = None
    if ct_type.startswith('application/octet-stream'):
        file_name = StrUtil.sub_string_after_last(ct_dis, "=")
        file_name = UrlUtil.decode(file_name)
        # print(file_name)
        file_name = file_name.replace("UTF-8''", '')
        if Validator.isEmpty(file_name):
            file_name = OsUtil.base_name(_url_)
        # print(file_name)
        f_name = file_name
    elif ct_type.startswith('image'):
        file_name = OsUtil.base_name(_url_)
        f_name = file_name
    # print(f_name)
    # 创建文件
    file_path = os.path.join(_path_, f_name)
    OsUtil.touch(file_path)
    open(file_path, 'wb').write(r.content)
    # 结果
    # print("下载成功")
    return file_path


if __name__ == '__main__':
    print("123")
    # mq_url = 'http://localhost:8080/mq/socket/test'
    # msg = JsonUtil.obj2str({
    #     'key': '10086',
    #     'msg': '数据集合读取成功',
    #     'source': 'log',
    #     'type': 'log'
    # })
    # print(msg)
    #
    # r = requests.post(mq_url,data={
    #     'key':'10086',
    #     'msg': msg
    # })
    # #
    # print(r.content)
    # url = "http://150.158.135.236:8888/down/EykdAGTWt6p3.xlsx"
    # url = 'http://mq.apisev.cn/disk/download/1634022017030295552'
    # url = 'http://mq.apisev.cn/'
    # dir_path = os.path.join(os.path.join(OsUtil.root("FastPY"), "disk"))
    # print(dir_path)
    # url = 'http://mq.apisev.cn/disk/download/1634022017030295552'
    # print(download(url, dir_path, Encode.ISO_8859_1))
    # url = "http://150.158.135.236:8888/down/EykdAGTWt6p3.xlsx"
    # print(download(url, dir_path))
