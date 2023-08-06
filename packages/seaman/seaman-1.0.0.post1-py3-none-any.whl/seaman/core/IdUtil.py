import uuid
from uuid import UUID
from seaman.core import Validator


# 生成一个随机的 UUID
def random_uuid() -> UUID:
    uuid1 = uuid.uuid1()
    # print(uuid1)
    return uuid1


def randomUUID() -> UUID:
    return random_uuid()


# 生成一个基于命名空间和名称的 UUID
def space_uuid(name: str, namespace: UUID) -> UUID:
    if Validator.isEmpty(namespace):
        namespace = time_uuid()
    # name = "example"
    uuid3 = uuid.uuid3(namespace, name)
    # print(uuid3)
    return uuid3


def spaceUUID(name: str, namespace: UUID) -> UUID:
    return space_uuid(name, namespace)

# def space_uuid(name: str) -> UUID:
#     namespace = time_uuid()
#     return space_uuid(name, namespace)


# 生成一个基于随机数和时间戳的 UUID
def time_uuid() -> UUID:
    uuid4 = uuid.uuid4()
    # print(uuid4)
    return uuid4


# 生成一个基于硬件地址和时间戳的 UUID
def ware_uuid(name: str, namespace: UUID) -> UUID:
    if Validator.isEmpty(namespace):
        namespace = time_uuid()
    uuid5 = uuid.uuid5(namespace, name)
    # print(uuid5)
    return uuid5


if __name__ == '__main__':
    print(randomUUID())
    # print(spaceUUID('kin'))
