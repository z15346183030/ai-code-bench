"""评分引擎 — 评估模型生成代码的正确性和质量。"""

import ast
import io
import sys
import traceback
from dataclasses import dataclass
from challenges.base import Challenge


def _check_code_safety(code: str) -> tuple[bool, str]:
    """检查代码是否包含危险操作。"""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, f"语法错误: {e}"

    dangerous_modules = {"os", "sys", "subprocess", "shutil", "socket", "http", "ftplib",
                         "ctypes", "importlib", "pathlib", "signal", "multiprocessing"}

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in dangerous_modules:
                    return False, f"禁止导入模块: {alias.name}"
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in dangerous_modules:
                return False, f"禁止导入模块: {node.module}"

    return True, ""


@dataclass
class EvalResult:
    """单题评估结果。"""
    challenge_name: str
    passed: int           # 通过的测试用例数
    total: int            # 总测试用例数
    correctness: float    # 正确性得分 (0-100)
    quality: float        # 代码质量得分 (0-100)
    score: float          # 综合得分 (0-100)
    code: str             # 模型生成的代码
    error: str = ""       # 错误信息


def run_test_case(code: str, func_name: str, challenge: Challenge, test_case) -> bool:
    """执行单个测试用例，返回是否通过。"""
    namespace = {}
    safe, msg = _check_code_safety(code)
    if not safe:
        return False
    try:
        exec(code, namespace)
    except Exception:
        return False

    func = namespace.get(func_name)
    if func is None:
        return False

    try:
        # 处理类的情况（如 LRU Cache）
        if challenge.name == "lru_cache":
            return _test_lru_cache(namespace, test_case)

        result = func(**test_case.input)

        # 链表题需要特殊比较
        if challenge.name == "merge_sorted_list":
            return _compare_linked_list(result, test_case.expected)

        return result == test_case.expected
    except Exception:
        return False


def _test_lru_cache(namespace: dict, test_case) -> bool:
    """LRU Cache 专项测试。"""
    try:
        ops = test_case.input["operations"]
        cache = namespace["LRUCache"](test_case.input["capacity"])
        results = []
        for method, args, _ in ops:
            if method == "put":
                cache.put(*args)
            elif method == "get":
                results.append(cache.get(*args))
        return results == test_case.expected
    except Exception:
        return False


def _compare_linked_list(result, expected) -> bool:
    """比较链表结果。"""
    try:
        values = []
        current = result
        while current:
            values.append(current.val)
            current = current.next
        return values == expected
    except Exception:
        return False


def evaluate_code_quality(code: str) -> float:
    """评估代码质量 (0-100)。"""
    score = 100.0

    # 1. 基本语法检查
    try:
        ast.parse(code)
    except SyntaxError:
        return 0.0

    lines = code.strip().split("\n")
    code_lines = [l for l in lines if l.strip() and not l.strip().startswith("#")]

    # 2. 代码长度检查（过长扣分）
    if len(code_lines) > 30:
        score -= min(20, (len(code_lines) - 30) * 2)

    # 3. 有注释加分（但不强求）
    has_comment = any(l.strip().startswith("#") for l in lines)
    if has_comment:
        score = min(100, score + 5)

    # 4. 函数命名规范（snake_case）
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not node.name.islower() and "_" not in node.name:
                    score -= 10
                    break
    except Exception:
        pass

    # 5. 无明显坏味道
    if "import *" in code:
        score -= 10
    if "exec(" in code or "eval(" in code:
        score -= 15
    if code.count("if ") > 15:  # 过多条件分支
        score -= 10

    return max(0, min(100, score))


def evaluate(challenge: Challenge, code: str) -> EvalResult:
    """评估模型在一道题上的表现。"""
    # 提取代码
    ok, extracted = challenge.validate_output(code)
    if not ok:
        return EvalResult(
            challenge_name=challenge.name,
            passed=0,
            total=len(challenge.test_cases),
            correctness=0,
            quality=0,
            score=0,
            code=code,
            error=extracted,
        )

    # 提取函数名
    func_name = _extract_func_name(extracted, challenge)

    # 运行测试用例
    passed = 0
    for tc in challenge.test_cases:
        if run_test_case(extracted, func_name, challenge, tc):
            passed += 1

    total = len(challenge.test_cases)
    correctness = (passed / total * 100) if total > 0 else 0

    # 代码质量
    quality = evaluate_code_quality(extracted)

    # 综合得分: 60% 正确性 + 40% 代码质量
    score = correctness * 0.6 + quality * 0.4

    return EvalResult(
        challenge_name=challenge.name,
        passed=passed,
        total=total,
        correctness=round(correctness, 1),
        quality=round(quality, 1),
        score=round(score, 1),
        code=extracted,
    )


def _extract_func_name(code: str, challenge: Challenge) -> str:
    """从代码中提取函数名。"""
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                return node.name
    except Exception:
        pass
    # 回退：从签名中提取
    if "def " in challenge.signature:
        return challenge.signature.split("def ")[1].split("(")[0].strip()
    return ""
