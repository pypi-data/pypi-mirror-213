from cachetools import LRUCache, FIFOCache, LFUCache


# Cache
class Cache:
    mode: str
    size: int
    cache: {}

    def __init__(self, mode: str, size: int):
        self.mode = mode
        self.size = size
        if mode.__eq__('FIFO'):
            self.cache = FIFOCache(size)
        elif mode.__eq__('LRU'):
            self.cache = LRUCache(size)
        elif mode.__eq__('LFU'):
            self.cache = LFUCache(size)
        else:
            self.cache = FIFOCache(size)

    # 缓存写入
    def set(self, key: str, val: any):
        self.cache[key] = val

    # 缓存读取
    def get(self, key: str):
        return self.cache[key]

    def keys(self):
        return self.cache.keys()


# 主函数测试
if __name__ == '__main__':
    fifo_cache = Cache('FIFO', 2)
    fifo_cache.set('1', 'hello')
    fifo_cache.set('2', 'world')
    print(fifo_cache.get('2'))
    print(fifo_cache.keys())
    fifo_cache.set('3', '!')
    print(fifo_cache.keys())
