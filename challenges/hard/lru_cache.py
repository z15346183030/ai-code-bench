"""LRU 缓存 — LeetCode #146"""

from challenges.base import Challenge, TestCase


class LRUCacheScenario:
    """模拟 LRU 缓存操作序列。"""
    def __init__(self, capacity, operations):
        self.capacity = capacity
        self.operations = operations  # list of (method, args, expected)


class LRUCache(Challenge):
    name = "lru_cache"
    difficulty = "hard"
    description = (
        "设计一个满足 LRU (最近最少使用) 缓存约束的数据结构。"
        "实现 LRUCache 类：\n"
        "- LRUCache(capacity) 以正整数 capacity 初始化容量\n"
        "- get(key) 如果关键字存在，返回值；否则返回 -1\n"
        "- put(key, value) 如果关键字已存在，变更其值；"
        "如果不存在，插入新值。当缓存容量达到上限时，"
        "在插入新项之前淘汰最久未使用的项。\n"
        "要求 get 和 put 的时间复杂度均为 O(1)。"
    )
    signature = "class LRUCache:\n    def __init__(self, capacity: int): ...\n    def get(self, key: int) -> int: ...\n    def put(self, key: int, value: int) -> None: ..."
    test_cases = [
        TestCase(
            input={
                "capacity": 2,
                "operations": [
                    ("put", [1, 1], None),
                    ("put", [2, 2], None),
                    ("get", [1], 1),
                    ("put", [3, 3], None),       # 淘汰 key=2
                    ("get", [2], -1),
                    ("put", [4, 4], None),       # 淘汰 key=1
                    ("get", [1], -1),
                    ("get", [3], 3),
                    ("get", [4], 4),
                ],
            },
            expected=[1, -1, -1, 3, 4],
        ),
        TestCase(
            input={
                "capacity": 1,
                "operations": [
                    ("put", [2, 1], None),
                    ("get", [2], 1),
                    ("put", [3, 2], None),       # 淘汰 key=2
                    ("get", [2], -1),
                    ("get", [3], 2),
                ],
            },
            expected=[1, -1, 2],
        ),
    ]
    solution = """
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.order = []

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.order.remove(key)
        self.order.append(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        self.cache[key] = value
        self.order.append(key)
"""
