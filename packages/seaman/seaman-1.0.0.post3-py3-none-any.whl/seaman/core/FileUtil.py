from seaman.core import OsUtil


# 返回目录下全部文件列表 包括是否为文件和文件名信息
def ls(_path_: str) -> list[OsUtil.File]:
    return OsUtil.ls(_path_)


# 判断是否是目录
def is_dir(_path_: str) -> bool:
    return OsUtil.is_dir(_path_)


def isDir(_path_: str) -> bool:
    return is_dir(_path_)


# 判断是否是文件
def is_file(_path_: str) -> bool:
    return OsUtil.is_file(_path_)


def isFile(_path_: str) -> bool:
    return is_file(_path_)


# 判断目录是否存在
def is_exist(_path_: str) -> bool:
    return OsUtil.is_exist(_path_)


def isExist(_path_: str) -> bool:
    return is_exist(_path_)


# 创建对应路径目录
def mkdir(_path_: str) -> bool:
    return OsUtil.mkdir(_path_)


# 创建对应路径文件
def touch(_path_: str) -> bool:
    return OsUtil.touch(_path_)


# 文件工具类
if __name__ == '__main__':
    print("FileUtil")
