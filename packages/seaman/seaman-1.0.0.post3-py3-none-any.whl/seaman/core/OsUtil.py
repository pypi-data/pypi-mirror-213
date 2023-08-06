import os
import shutil


# 定义文件信息 class
class File:
    is_dir = False
    file_name = None

    def __init__(self, a: bool, b: str):
        self.is_dir = a
        self.file_name = b


# 获取当前执行代码根目录
def code_path() -> str:
    return os.getcwd()


def codePath() -> str:
    return code_path()


# 判断系统类型
def system() -> str:
    os_name = os.name
    if os_name == 'nt':
        # print("windows")
        return 'windows'
    elif os_name == 'posix':
        # print("linux")
        return 'linux'


# 返回目录下全部文件列表 包括是否为文件和文件名信息
def ls(_path_: str) -> list[File]:
    files: list[File] = []
    # 不是文件夹返回空
    if not is_dir(_path_):
        return files
    for item in os.listdir(_path_):
        # print(os.path.isdir(_path_+os.sep+item))
        files.append(File(os.path.isdir(_path_ + os.sep + item), item))
        # print(item)
    return files


# 判断是否是目录
def is_dir(_path_: str) -> bool:
    return os.path.isdir(_path_)


def isDir(_path_: str) -> bool:
    return is_dir(_path_)


# 判断是否是文件
def is_file(_path_: str) -> bool:
    return os.path.isfile(_path_)


def isFile(_path_: str) -> bool:
    return is_file(_path_)


# 判断目录是否存在
def is_exist(_path_: str) -> bool:
    return os.path.exists(_path_)


def isExist(_path_: str) -> bool:
    return is_exist(_path_)


# 创建对应路径目录
def mkdir(_path_: str) -> bool:
    if os.path.exists(_path_):
        return True
    else:
        os.mkdir(_path_)
        return True


# 创建对应路径文件
def touch(_path_: str) -> bool:
    dir_path = os.path.dirname(_path_)
    mkdir(dir_path)
    if os.path.exists(_path_):
        return True
    else:
        try:
            open(_path_, 'x')
        except FileExistsError:
            pass
        return True


# 删除文件 或者 文件夹 test pass
def rm(_path_: str) -> None:
    # 如果 文件夹
    if is_dir(_path_):
        shutil.rmtree(_path_)
    else:
        os.remove(_path_)


# 文件/文件夹 复制
def copy(_source_: str, _target_: str) -> bool:
    if not is_exist(_source_):
        return True
    if not is_exist(_target_):
        mkdir(_target_)
    if system() == 'windows':
        os.system('copy ' + _source_ + ' ' + _target_)
    elif system() == 'linux':
        os.system('cp ' + _source_ + ' ' + _target_)
    # 如果两个都是文件
    # if is_file(_source_) and is_file(_target_):
    return True


# 获取项目根目录
# 传入项目名称获取最终根目录
def root(_project_: str) -> str:
    current_file_path = os.path.abspath(__file__)
    # 从当前文件的路径中获取项目的根目录
    root_directory = current_file_path
    while not os.path.basename(root_directory).startswith(_project_):
        root_directory = os.path.dirname(root_directory)
    # current_file_path = os.path.abspath(__file__)
    # 创建完整的路径
    return root_directory
    # return file_path


# 子文件目录路径
def sub_root(_project_: str, _sub_: str) -> str:
    return os.path.join(root(_project_), _sub_)


def subRoot(_project_: str, _sub_: str) -> str:
    return sub_root(_project_, _sub_)


# 获取路径上项目基础名称
def base_name(_path_: str) -> str:
    if is_file(_path_):
        return os.path.basename(_path_)
    else:
        return ''


def baseName(_path_: str) -> str:
    return base_name(_path_)


if __name__ == '__main__':
    # print(root("FastPY"))
    print(sub_root('FastPY', 'matlab'))
