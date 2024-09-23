import solve

def string_length(s: str) -> int:
    """
    Manually converts a number in a given base to base 10 (decimal) and returns it as a string.

    Parameters:
    number (str): The number in the given base as a string.
    base (int): The base of the input number (between 2 and 16).

    Returns:
    str: The number converted to base 10 as a string.
    """
    if base < 2 or base > 16:
        raise ValueError("Base must be between 2 and 16 (inclusive).")
    
    digits = "0123456789ABCDEF"
    number = number.upper()
    is_negative = False
    if number.startswith('-'):
        is_negative = True
        number = number[1:]
    
    result = "0"
    for char in number:
        if char not in digits[:base]:
            raise ValueError(f"Invalid digit '{char}' for base {base}.")
        digit_value = digits.index(char)
        result = addition(str(multiplication(result, str(base), base)), digit_value)
    
    return "-" + result if is_negative else result

def make_neg(num: str) -> str:
    """
    Makes a number negative if it is not already, or removes the negative sign if it is.

    :param num: The number to be negated.
    :type num: str
    :return: The negated number.
    :rtype: str
    """
    return num[1:] if num[0] == '-' else '-' + num

def is_greater(a: str, b: str, base: int) -> bool:
    """
    Compares two numbers in a given base to determine if the first is greater than the second.

    :param a: The first number.
    :type a: str
    :param b: The second number.
    :type b: str
    :param base: The base of the numbers.
    :type base: int
    :return: True if a is greater than b, False otherwise.
    :rtype: bool
    """
    if a[0] == '-' and b[0] != '-':
        return False
    if a[0] != '-' and b[0] == '-':
        return True

    if a[0] == '-' and b[0] == '-':
        return not is_greater(a[1:], b[1:], base)

    if len(a) != len(b):
        return len(a) > len(b)
    
    for i in range(len(a)):
        diff = substraction(a[i], b[i], base)
        if diff[0] == '-':
            return False
        if diff != '0':
            return True

    return False

def addition(x: str, y: str, base: int) -> str:
    """
    Adds two numbers in a given base.

    :param x: The first number.
    :type x: str
    :param y: The second number.
    :type y: str
    :param base: The base of the numbers.
    :type base: int
    :return: The sum of the two numbers.
    :rtype: str
    """
    symbols: list[str] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

    if x[0] == '-' and y[0] == '-':
        return make_neg(addition(make_neg(x), make_neg(y), base))
    if x[0] == '-':
        return substraction(y, make_neg(x), base)
    if y[0] == '-':
        return substraction(x, make_neg(y), base)

    max_len = len(x) if is_greater(x, y, base) else len(y)
    x, y = x.zfill(max_len), y.zfill(max_len)

    carry = 0
    result = ''

    for i in range(max_len - 1, -1, -1):
        total = carry + int(convert_to_base_10(x[i], base)) + int(convert_to_base_10(y[i], base))
        carry = total // base
        result = symbols[total % base] + result

    if carry:
        result = symbols[carry] + result

    return result.lstrip('0') or '0'

def mod_addition(x: str, y: str, mod: str, base: int) -> str:
    """
    Adds two numbers in a given base and then takes the modulus.

    :param x: The first number.
    :type x: str
    :param y: The second number.
    :type y: str
    :param mod: The modulus.
    :type mod: str
    :param base: The base of the numbers.
    :type base: int
    :return: The result of (x + y) % mod.
    :rtype: str
    """
    temp_sum = addition(x, y, base)
    
    while is_greater(temp_sum, mod, base) or temp_sum == mod:
        temp_sum = substraction(temp_sum, mod, base)
    while is_greater('0', temp_sum, base):
        temp_sum = addition(temp_sum, mod, base)
        
    return temp_sum

def substraction(x: str, y: str, base: int) -> str:
    """
    Subtracts the second number from the first in a given base.

    :param x: The first number.
    :type x: str
    :param y: The second number.
    :type y: str
    :param base: The base of the numbers.
    :type base: int
    :return: The result of x - y.
    :rtype: str
    """
    symbols: list[str] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

    if x[0] == '-' and y[0] == '-':
        return substraction(make_neg(y), make_neg(x), base)
    if x[0] == '-':
        return make_neg(addition(make_neg(x), y, base))
    if y[0] == '-':
        return addition(x, make_neg(y), base)

    if len(y) > len(x) or (len(x) == len(y) and is_greater(y, x, base)):
        return make_neg(substraction(y, x, base))

    max_len = len(x) if len(x) > len(y) else len(y)
    x, y = x.zfill(max_len), y.zfill(max_len)

    carry = 0
    result = ''

    for i in range(max_len - 1, -1, -1):
        diff = int(convert_to_base_10(x[i], base)) - int(convert_to_base_10(y[i], base)) - carry
        carry = 1 if diff < 0 else 0
        result = symbols[diff % base] + result

    return result.lstrip('0') or '0'

def mod_subtraction(x: str, y: str, mod: str, base: int) -> str:
    """
    Subtracts the second number from the first in a given base and then takes the modulus.

    :param x: The first number.
    :type x: str
    :param y: The second number.
    :type y: str
    :param mod: The modulus.
    :type mod: str
    :param base: The base of the numbers.
    :type base: int
    :return: The result of (x - y) % mod.`
    :rtype: str
    """
    temp_diff = substraction(x, y, base)
    
    while is_greater(temp_diff, mod, base) or temp_diff == mod:
        temp_diff = substraction(temp_diff, mod, base)
    while is_greater('0', temp_diff, base):
        temp_diff = addition(temp_diff, mod, base)
        
    return temp_diff

def multiplication(x: str, y: str, base: int) -> str:
    """
    Multiplies two numbers in a given base.

    :param x: The first number.
    :type x: str
    :param y: The second number.
    :type y: str
    :param base: The base of the numbers.
    :type base: int
    :return: The product of the two numbers.
    :rtype: str
    """
    symbols: list[str] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

    if x[0] == '-' and y[0] == '-':
        return multiplication(make_neg(x), make_neg(y), base)
    if x[0] == '-':
        return make_neg(multiplication(make_neg(x), y, base))
    if y[0] == '-':
        return make_neg(multiplication(x, make_neg(y), base))

    max_len = len(x) if len(x) > len(y) else len(y)
    x, y = x.zfill(max_len), y.zfill(max_len)

    result = '0'
    for i, digit_x in enumerate(reversed(x)):
        temp_result = ''
        carry = 0
        for digit_y in reversed(y):
            product = int(digit_x, base) * int(digit_y, base) + carry
            carry = product // base
            temp_result = symbols[product % base] + temp_result
        if carry:
            temp_result = symbols[carry] + temp_result
        result = addition(result + '0' * i, temp_result, base)

    return result

def mod(x: str, mod: str, base: int) -> str:
    """
    Find the modulus of a number in a given base.
    
    :param x: The number.
    :type x: str
    :param mod: The modulus.
    :type mod: str
    :param base: The base of the numbers.
    :type base: int
    :return: The result of x % mod.
    :rtype: str
    """
    temp = x
    if mod == '0':
        raise ValueError("Modulus cannot be 0.")
    if mod[0] == '-':
        mod = mod[1:]
    while is_greater(temp, mod, base) or temp == mod:
        temp = substraction(temp, mod, base)
    return temp

def floor_div(x: str, y: str, base: int) -> str:
    """
    Divides the first number by the second and returns the floor of the result.

    :param x: The dividend.
    :type x: str
    :param y: The divisor.
    :type y: str
    :param base: The base of the numbers.
    :type base: int
    :return: The floor of x / y.
    :rtype: str
    """
    if y == '0':
        raise ValueError("Cannot divide by zero.")
    
    if x[0] == '-' and y[0] == '-':
        return floor_div(make_neg(x), make_neg(y), base)
    if x[0] == '-':
        return make_neg(floor_div(make_neg(x), y, base))
    if y[0] == '-':
        return make_neg(floor_div(x, make_neg(y), base))

    if is_greater(y, x, base):
        return '0'
    if x == y:
        return '1'

    temp = x
    result = '0'
    while is_greater(temp, y, base) or temp == y:
        temp = substraction(temp, y, base)
        result = addition(result, '1', base)

    return result


import random
def subtractx(a_str, b_str, base):
    def create(base):
        mp = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
        digits = [mp[i] if i in mp else str(i) for i in range(base)]
        return digits

    def padding(x, y):
        x = str(x)
        y = str(y)
        while len(x) < len(y):
            x = '0' + x
        while len(y) < len(x):
            y = '0' + y
        return x, y

    def compare_numbers(a_str, b_str, basenum):
        # Compare two numbers represented as strings
        for a_digit, b_digit in zip(a_str, b_str):
            index_a = basenum.index(a_digit)
            index_b = basenum.index(b_digit)
            if index_a > index_b:
                return 1  # a_str > b_str
            elif index_a < index_b:
                return -1  # a_str < b_str
        return 0  # a_str == b_str

    def digit_subtract(a_digit, b_digit, borrow, basenum):
        # Subtract two digits along with borrow
        index_a = basenum.index(a_digit)
        index_b = basenum.index(b_digit)
        index_borrow = borrow

        # Adjust index_b with borrow
        index_b += index_borrow

        if index_a >= index_b:
            index_diff = index_a - index_b
            borrow_out = 0
        else:
            index_diff = index_a + len(basenum) - index_b
            borrow_out = 1

        diff_digit = basenum[index_diff]
        return diff_digit, borrow_out

    # Handle negative inputs
    negative_a = False
    negative_b = False

    if a_str.startswith('-'):
        negative_a = True
        a_str = a_str[1:]
    if b_str.startswith('-'):
        negative_b = True
        b_str = b_str[1:]

    basenum = create(base)
    a_str, b_str = padding(a_str, b_str)

    # Determine operation based on the signs of a and b
    if negative_a and negative_b:
        # (-a) - (-b) = b - a
        result = subtractx(b_str, a_str, base)
    elif negative_a and not negative_b:
        # (-a) - b = -(a + b)
        result = add(a_str, b_str, base)
        result = '-' + result
    elif not negative_a and negative_b:
        # a - (-b) = a + b
        result = add(a_str, b_str, base)
    else:
        # a - b
        comparison = compare_numbers(a_str, b_str, basenum)
        if comparison == 0:
            return '0'
        elif comparison < 0:
            # If a < b, swap and remember to add negative sign later
            a_str, b_str = b_str, a_str
            negative_result = True
        else:
            negative_result = False

        result_digits = []
        borrow = 0  # Use integer for borrow

        # Process digits from least significant to most significant
        for i in range(len(a_str) - 1, -1, -1):
            a_digit = a_str[i]
            b_digit = b_str[i]

            # Use digit_subtract to compute the digit difference and new borrow
            diff_digit, borrow = digit_subtract(a_digit, b_digit, borrow, basenum)

            result_digits.insert(0, diff_digit)

        # Remove leading zeros from the result
        while len(result_digits) > 1 and result_digits[0] == '0':
            del result_digits[0]

        result_str = ''.join(result_digits)
        if negative_result:
            result_str = '-' + result_str
        result = result_str

    return result

def add(a_str, b_str, base):
    def create(base):
        mp = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
        digits = [mp[i] if i in mp else str(i) for i in range(base)]
        return digits

    def padding(x, y):
        x = str(x)
        y = str(y)
        while len(x) < len(y):
            x = '0' + x
        while len(y) < len(x):
            y = '0' + y
        return x, y

    def compare_numbers(a_str, b_str, basenum):
        # Compare two numbers represented as strings
        for a_digit, b_digit in zip(a_str, b_str):
            index_a = basenum.index(a_digit)
            index_b = basenum.index(b_digit)
            if index_a > index_b:
                return 1  # a_str > b_str
            elif index_a < index_b:
                return -1  # a_str < b_str
        return 0  # a_str == b_str

    # Handle negative inputs
    negative_a = False
    negative_b = False

    if a_str.startswith('-'):
        negative_a = True
        a_str = a_str[1:]
    if b_str.startswith('-'):
        negative_b = True
        b_str = b_str[1:]

    basenum = create(base)
    a_str, b_str = padding(a_str, b_str)

    # Determine operation based on the signs of a and b
    if negative_a == negative_b:
        # Both numbers have the same sign
        # Perform addition of magnitudes
        result_digits = []
        carry = 0  # Use integer for carry

        # Process digits from least significant to most significant
        for i in range(len(a_str) - 1, -1, -1):
            a_digit = a_str[i]
            b_digit = b_str[i]

            # Sum digits without using '+'
            index_a = basenum.index(a_digit)
            index_b = basenum.index(b_digit)
            index_carry = carry

            total = index_a + index_b + index_carry

            # Determine new carry
            if total >= len(basenum):
                carry = 1
                total -= len(basenum)
            else:
                carry = 0

            # Append result digit
            result_digits.insert(0, basenum[total])

        if carry == 1:
            result_digits.insert(0, '1')

        # Remove leading zeros
        while len(result_digits) > 1 and result_digits[0] == '0':
            del result_digits[0]

        result_str = ''.join(result_digits)
        if negative_a:
            result_str = '-' + result_str
    else:
        # Numbers have different signs
        # Subtract the smaller magnitude from the larger magnitude
        comparison = compare_numbers(a_str, b_str, basenum)
        if comparison == 0:
            return '0'
        elif comparison > 0:
            # a_str magnitude > b_str magnitude
            negative_result = negative_a  # Result has the sign of 'a'
            a_str_mag = a_str
            b_str_mag = b_str
        else:
            # b_str magnitude > a_str magnitude
            negative_result = negative_b  # Result has the sign of 'b'
            a_str_mag = b_str
            b_str_mag = a_str

        result_digits = []
        borrow = 0  # Use integer for borrow

        # Process digits from least significant to most significant
        for i in range(len(a_str_mag) - 1, -1, -1):
            a_digit = a_str_mag[i]
            b_digit = b_str_mag[i]

            # Subtract digits without using '-'
            index_a = basenum.index(a_digit)
            index_b = basenum.index(b_digit) + borrow

            if index_a >= index_b:
                index_diff = index_a - index_b
                borrow = 0
            else:
                index_a += len(basenum)
                index_diff = index_a - index_b
                borrow = 1

            # Append result digit
            result_digits.insert(0, basenum[index_diff])

        # Remove leading zeros
        while len(result_digits) > 1 and result_digits[0] == '0':
            del result_digits[0]

        result_str = ''.join(result_digits)
        if negative_result:
            result_str = '-' + result_str

    return result_str








def karatsuba(x: str, y: str, base: int) -> str:
    """
    Multiplies two numbers using the Karatsuba algorithm in a given base.

    :param x: The first number.
    :type x: str
    :param y: The second number.
    :type y: str
    :param base: The base of the numbers.
    :type base: int
    :return: The product of the two numbers.
    :rtype: str
    """
    if len(x) == 1 or len(y) == 1:
        return multiplication(x, y, base)

    max_len = len(x) if len(x) > len(y) else len(y)
    if max_len % 2 != 0:
        max_len += 1

    x, y = x.zfill(max_len), y.zfill(max_len)
    half_len = max_len // 2

    x_low, x_high = x[:half_len], x[half_len:]
    y_low, y_high = y[:half_len], y[half_len:]

    high_product = karatsuba(x_high, y_high, base)
    low_product = karatsuba(x_low, y_low, base)
    cross_sum = substraction(
        substraction(
            karatsuba(addition(x_high, x_low, base), addition(y_high, y_low, base), base),
            high_product, base),
        low_product, base)

    result = addition(addition(high_product + '0' * max_len, cross_sum + '0' * half_len, base), low_product, base)
    return result

def length(x, r):
    """
    Get length of string x in radix r.
    """
    k = '0'
    while len(x) > 0:
        x = x[1:]
        k = addition(k, '1', r)
    return k


#print(subtractx("1000000000000000000","-1",10))