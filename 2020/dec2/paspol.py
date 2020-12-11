from typing import List, Optional

TARGET = 2020


def num_valid_passwords(min_freqs: List[int],
    max_freqs: List[int],
    chars: List[str],
    passwords: List[str]
    ) -> int:
    num_valid = 0
    for ind, password in enumerate(passwords):
        password = password.strip()
        num_char = int(password[min_freqs[ind] - 1] == chars[ind]) + int(password[max_freqs[ind] - 1] == chars[ind])
        if num_char == 1:
            num_valid += 1
    return num_valid


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        policies, passwords = [x.split(":")[0] for x in lines], [x.split(":")[1] for x in lines]
        freqs, chars = [x.split()[0] for x in policies], [x.split()[1] for x in policies]
        min_freqs, max_freqs = [x.split('-')[0] for x in freqs], [x.split('-')[1] for x in freqs]
        min_freqs = [int(x) for x in min_freqs]
        max_freqs = [int(x) for x in max_freqs]

    print(num_valid_passwords(min_freqs, max_freqs, chars, passwords))
