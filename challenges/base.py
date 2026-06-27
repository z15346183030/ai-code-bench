"""题目基类和数据结构定义。"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TestCase:
    """单个测试用例。"""
    input: dict[str, Any]
    expected: Any
    description: str = ""


class Challenge:
    """编程题目基类。所有题目继承此类。"""

    # 子类覆盖这些类属性
    name: str = ""
    difficulty: str = "easy"
    description: str = ""
    signature: str = ""
    test_cases: list[TestCase] = []
    solution: str = ""

    def __init_subclass__(cls, **kwargs):
        """确保子类有独立的 test_cases 列表。"""
        super().__init_subclass__(**kwargs)
        if "test_cases" not in cls.__dict__:
            cls.test_cases = []

    def build_prompt(self) -> str:
        """构建发送给模型的 Prompt。"""
        test_examples = ""
        for i, tc in enumerate(self.test_cases[:3], 1):
            test_examples += f"  示例{i}: input={tc.input}, output={tc.expected}\n"

        return f"""请完成以下编程题目，只返回 Python 代码，不要包含任何解释文字。

题目: {self.description}

函数签名: {self.signature}

测试示例:
{test_examples}要求:
1. 只返回一个完整的 Python 函数实现
2. 不要修改函数签名
3. 不要包含 print 语句或测试代码
4. 代码需要能直接被 import 使用
"""

    def validate_output(self, code: str) -> tuple[bool, str]:
        """从模型输出中提取代码。"""
        code = code.strip()
        if code.startswith("```python"):
            code = code[9:]
        elif code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
        code = code.strip()

        if "def " not in code:
            return False, "未找到函数定义"

        return True, code
