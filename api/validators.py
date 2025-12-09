def validate_phone_rules(number: str):
    if not isinstance(number, str) or len(number) != 6 or not number.isdigit():
        return {
            "format_ok": False,
            "has_non_zero_digit": False,
            "sum_first_equals_last": False,
            "sum_odd_equals_even": False,
            "is_valid": False
        }

    digits = [int(ch) for ch in number]
    has_non_zero = any(d != 0 for d in digits)
    sum_first = sum(digits[0:3])
    sum_last = sum(digits[3:6])
    sum_odd = digits[0] + digits[2] + digits[4]
    sum_even = digits[1] + digits[3] + digits[5]
    is_valid = has_non_zero and (sum_first == sum_last) and (sum_odd == sum_even)

    return {
        "format_ok": True,
        "has_non_zero_digit": has_non_zero,
        "sum_first_equals_last": (sum_first == sum_last),
        "sum_odd_equals_even": (sum_odd == sum_even),
        "is_valid": is_valid
    }
