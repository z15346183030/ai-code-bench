"""两数之和 — LeetCode #1"""

from challenges.base import Challenge, TestCase


class TwoSum(Challenge):
    name = "two_sum"
    difficulty = "easy"
    description = (
        "给定一个整数数组 nums 和一个整数目标值 target，"
        "请在数组中找出和为 target 的两个整数，返回它们的下标。"
        "假设每种输入只有一个答案，且同一个元素不能使用两次。"
    )
    signature = "def two_sum(nums: list[int], target: int) -> list[int]:"
    test_cases = [
        TestCase(input={"nums": [2, 7, 11, 15], "target": 9}, expected=[0, 1]),
        TestCase(input={"nums": [3, 2, 4], "target": 6}, expected=[1, 2]),
        TestCase(input={"nums": [3, 3], "target": 6}, expected=[0, 1]),
        TestCase(input={"nums": [1, 5, 3, 7], "target": 12}, expected=[1, 3]),
    ]
    solution = """
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
"""
