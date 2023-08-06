import json
from typing import TypeVar, Type

T = TypeVar('T')


# 测试类
class Person:
    name: str
    age: int

    def __init__(self, name, age):
        self.name = name
        self.age = age


# json 形式字符串解析
def parse(_str_: str) -> json:
    return json.loads(_str_)


# json 转 字符串
def obj2str(obj: object):
    json_str = json.dumps(obj, ensure_ascii=False, default=lambda o: o.__dict__)
    return json_str


# 字符串转obj
def str2obj(_str_: str, clazz: Type[T]) -> T:
    json_dict = json.loads(_str_)
    return clazz(**json_dict)


if __name__ == '__main__':
    jack = Person('jack', 18)
    print(jack)
    j_str = obj2str(jack)
    print(j_str)
    d_jack = str2obj(j_str, Person)
    print(d_jack.name)
    # json1 = {"accessToken": "521de21161b23988173e6f7f48f9ee96e28",
    #          "User-Agent": "Apache-HttpClient/4.5.2 (Java/1.8.0_131)"}
    # print(obj2str(json1))
    # print(type(obj2str(json1)))
