"""有效括号 — LeetCode #20"""

from challenges.base import Challenge, TestCase


class ValidParentheses(Challenge):
    name = "valid_parentheses"
    difficulty = "medium"
    description = (
        "给定一个只包含 '(', ')', '{', '}', '[', ']' 的字符串，"
        "判断字符串是否有效。有效字符串需满足："
        "左括号必须用相同类型的右括号闭合，且按正确顺序闭合。"
    )
    signature = "def is_valid(s: str) -> bool:"
    test_cases = [
        TestCase(input={"s": "()"}, expected=True),
        TestCase(input={"s": "()[]{}"}, expected=True),
        TestCase(input={"s": "(]"}, expected=False),
        TestCase(input={"s": "([)]"}, expected=False),
        TestCase(input={"s": "{[]}"}, expected=True),
        TestCase(input={"s": ""}, expected=True),
        TestCase(input={"s": "((("}, expected=False),
    ]
    solution = """
def is_valid(s: str) -> bool:
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in mapping:
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            stack.append(char)
    return len(stack) == 0
"""
