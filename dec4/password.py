
def is_password_valid(value: int) -> bool:
    value_str = str(value)

    first_number = int(value_str[0])
    two_digits_equal = False
    for char in value_str[1:]:
        second_number = int(char)
        if first_number < second_number:
            first_number = second_number
        elif first_number == second_number:
            two_digits_equal = True
            first_number = second_number
        else:
            return False

    if not two_digits_equal:
        return False
    
    return True


if __name__ == '__main__':
    start_value = 158126
    stop_value = 624574

    valid_passwords = 0
    for value in range(start_value, stop_value + 1):
        if is_password_valid(value):
            print('valid password:', value)
            valid_passwords += 1

    print('num passwords:', valid_passwords)