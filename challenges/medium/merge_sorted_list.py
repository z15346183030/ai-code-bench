"""合并两个有序链表 — LeetCode #21"""

from challenges.base import Challenge, TestCase


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def list_to_array(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


def array_to_list(arr):
    dummy = ListNode(0)
    current = dummy
    for val in arr:
        current.next = ListNode(val)
        current = current.next
    return dummy.next


class MergeSortedLists(Challenge):
    name = "merge_sorted_lists"
    difficulty = "medium"
    description = (
        "将两个升序链表合并为一个新的升序链表并返回。"
        "新链表是通过拼接给定的两个链表的所有节点组成的。"
        "ListNode 定义: class ListNode: def __init__(self, val=0, next=None)"
    )
    signature = "def merge_two_lists(list1: ListNode, list2: ListNode) -> ListNode:"
    test_cases = [
        TestCase(
            input={"list1": array_to_list([1, 2, 4]), "list2": array_to_list([1, 3, 4])},
            expected=[1, 1, 2, 3, 4, 4],
        ),
        TestCase(
            input={"list1": None, "list2": None},
            expected=[],
        ),
        TestCase(
            input={"list1": None, "list2": array_to_list([0])},
            expected=[0],
        ),
    ]
    solution = """
def merge_two_lists(list1: ListNode, list2: ListNode) -> ListNode:
    dummy = ListNode(0)
    current = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
    current.next = list1 or list2
    return dummy.next
"""

    def validate_output(self, code: str) -> tuple[bool, str]:
        """重写验证：链表题需要特殊处理。"""
        ok, result = super().validate_output(code)
        if not ok:
            return ok, result
        # 确保代码引用了 ListNode
        if "ListNode" not in result and "list" not in result.lower():
            return False, "代码中未使用 ListNode"
        return True, result
