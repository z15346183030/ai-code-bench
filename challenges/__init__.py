"""题目加载器。自动发现并注册所有题目。"""

import importlib
import pkgutil
from challenges.base import Challenge

# 全局题目注册表
_registry: list[Challenge] = []


def register(challenge: Challenge):
    """注册一道题目。"""
    _registry.append(challenge)


def load_all() -> list[Challenge]:
    """自动加载所有题目模块。"""
    if _registry:
        return _registry

    # 遍历 easy/medium/hard 子目录
    for difficulty in ["easy", "medium", "hard"]:
        package_path = f"challenges.{difficulty}"
        try:
            package = importlib.import_module(package_path)
            for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
                module = importlib.import_module(f"{package_path}.{modname}")
                # 查找模块中所有 Challenge 子类实例
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, Challenge) and attr is not Challenge:
                        instance = attr()
                        if instance.name:
                            register(instance)
        except ImportError:
            continue

    return _registry


def get_by_difficulty(difficulty: str) -> list[Challenge]:
    """按难度筛选题目。"""
    return [c for c in load_all() if c.difficulty == difficulty]
