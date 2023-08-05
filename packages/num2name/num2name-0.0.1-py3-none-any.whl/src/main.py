num_dict = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
    20: "twenty",
    30: "thirty",
    40: "forty",
    50: "fifty",
    60: "sixty",
    70: "seventy",
    80: "eighty",
    90: "ninety",
    100: "hundred",
    1000: "thousand"
}


def num2name_up_to_99(num):
    if num <= 20:
        return num_dict[num]
    if 20 < num < 100:
        return f"{ num_dict[int(num / 10) * 10] } { num_dict[num % 10] if num % 10 else '' }"
    else:
        raise ValueError(f"{num} is greater than 99")


def num2name_up_to_999(num):
    if num < 100:
        return num2name_up_to_99(num)
    elif num < 1000:
        return f"{ num_dict[int(num / 100)] } hundred { num2name_up_to_99(num % 100) if num % 100 else '' }"
    else:
        raise ValueError(f"{num} is greater than 999")


def into_international(num):
    return num2name_up_to_999(num)


def into_indian(num):
    return num2name_up_to_999(num)


def convert(num, system="en"):
    if num < 0:
        raise ValueError(f"{num} is negative number which is not supported.")

    if num >= 1000:
        raise ValueError(f"{num} is greater than 1000 which is not supported in current version.")

    if system == "en":
        return into_international(num)
    elif system == "in":
        return into_indian(num)
    else:
        raise ValueError(f"{system} is not valid system type.")


if __name__ == '__main__':
    print(convert(230, "in"))
