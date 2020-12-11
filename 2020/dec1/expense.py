from typing import List, Optional

TARGET = 2020


def find_result(nums: List[int]) -> Optional[int]:
    # High efficiency quadratic time solution lol
    for x in nums:
        for y in nums:
            if x + y == 2020:
                return x * y


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        nums = [int(x) for x in lines]

    print(find_result(nums))
