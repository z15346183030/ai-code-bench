"""FizzBuzz — 经典编程题"""

from challenges.base import Challenge, TestCase


class FizzBuzz(Challenge):
    name = "fizzbuzz"
    difficulty = "easy"
    description = (
        "给定整数 n，返回从 1 到 n 的字符串数组。"
        "规则：能被3整除返回 'Fizz'，能被5整除返回 'Buzz'，"
        "能被3和5同时整除返回 'FizzBuzz'，其他情况返回数字字符串。"
    )
    signature = "def fizzbuzz(n: int) -> list[str]:"
    test_cases = [
        TestCase(input={"n": 3}, expected=["1", "2", "Fizz"]),
        TestCase(input={"n": 5}, expected=["1", "2", "Fizz", "4", "Buzz"]),
        TestCase(
            input={"n": 15},
            expected=[
                "1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz",
                "11", "Fizz", "13", "14", "FizzBuzz"
            ],
        ),
    ]
    solution = """
def fizzbuzz(n: int) -> list[str]:
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result
"""
