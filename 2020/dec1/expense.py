from typing import List, Optional

TARGET = 2020


def find_result(nums: List[int]) -> Optional[int]:
    # High efficiency cubics time solution lelz
    for x in nums:
        for y in nums:
            for z in nums:
                if x + y + z == 2020:
                    return x * y * z


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        nums = [int(x) for x in lines]

    print(find_result(nums))
