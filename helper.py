def convert_to_base_10(number: str, base: int) -> str:
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
    
    result = 0
    for char in number:
        if char not in digits[:base]:
            raise ValueError(f"Invalid digit '{char}' for base {base}.")
        digit_value = digits.index(char)
        result = result * base + digit_value
    
    return str(-result) if is_negative else str(result)

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
        # diff = substraction(a[i], b[i], base)
        # if diff[0] == '-':
        #     return False
        # if diff != '0':
        #     return True
        if a[i] != b[i]:
            return a[i] > b[i]

    return False

def modulus(x: str, y: str, base: int) -> str:
    """
    Computes the modulus of x by y in a given base.

    :param x: The dividend.
    :type x: str
    :param y: The divisor.
    :type y: str
    :param base: The base of the numbers.
    :type base: int
    :return: The result of x % y.
    :rtype: str
    """
    if y == '0':
        raise ValueError("Cannot divide by zero.")
    
    if x[0] == '-' and y[0] == '-':
        return modulus(make_neg(x), make_neg(y), base)
    if x[0] == '-':
        return make_neg(modulus(make_neg(x), y, base))
    if y[0] == '-':
        return modulus(x, make_neg(y), base)

    if is_greater(y, x, base):
        return x
    if x == y:
        return '0'

    temp = x
    while is_greater(temp, y, base) or temp == y:
        temp = subtractx(temp, y, base)

    # If the result is negative, add the divisor to it
    if temp[0] == '-':
        temp = add(temp, y, base)

    return temp

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
            # temp_result = symbols[int(modulus(str(product), str(base), base))] + temp_result
            temp_result = symbols[product % base] + temp_result
        if carry:
            temp_result = symbols[carry] + temp_result
        result = addition(result, temp_result + '0' * i, base)

    return result

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
        result = add(result, '1', base)

    return result

# import random
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

def length(x, r):
    """
    Get length of string x in radix r.
    """
    k = '0'
    while len(x) > 0:
        x = x[1:]
        k = addition(k, '1', r)
    return k

def modulus_substract(x: str, y: str, mod: str, radix: int):
    if mod == "0":
        return None
    z = subtractx(x, y, radix)  # x - y mod
    last_valid_z = z  # keep track of the last valid result
    while "-" not in z:
        last_valid_z = z  # update last valid result
        z = subtractx(z, mod, radix)  # subtract mod
    return last_valid_z  # return the last valid z before negative


def modulus_add(x: str, y: str, mod: str, radix: int):
    if mod =="0":
        return None
    z = add(x, y, radix)
    last_valid_z = z  # keep track of the last valid result

    while "-" not in z:
        last_valid_z = z  # update last valid result
        z = subtractx(z, mod, radix)  # subtract mod
    return last_valid_z  # return the last valid z before negative

def modulus_red(x: str, mod: str, radix: int):
    if mod == "0":
        return None
    
    # If x is non-negative, subtract mod until x is less than mod
    if "-" not in x:
        last_valid_x = x  # Track the last valid result
        while "-" not in subtractx(x, mod, radix):  # While x >= mod
            last_valid_x = subtractx(x, mod, radix)
            x = last_valid_x
        return last_valid_x
    
    # If x is negative, add mod until x becomes non-negative (keeping the sign)
    else:
        while "-" in x:
            x = add(x, mod, radix)  # Add mod directly to x, keeping the sign intact
        return x
#print(subtractx("1000000000000000000","-1",10))

def modulus_multiplication(x: str, y: str, mod: str, radix: int) -> str:
    a = modulus_red(x, mod, radix)
    b = modulus_red(y, mod, radix)
    z1 = multiplication(a, b, radix)
    z = modulus_red(z1, mod, radix)
    return z
# print(modulus_multiplication("10","3","7",10))

def inversion(x: str, m: str, base: int) -> str:
    """
    Computes the modular inverse of x modulo m using the Extended Euclidean Algorithm.

    :param x: The number to find the inverse of.
    :type x: str
    :param m: The modulus.
    :type m: str
    :param base: The base of the numbers.
    :type base: int
    :return: The modular inverse of x modulo m.
    :rtype: str
    """
    if m == '0':
        raise ValueError("Modulus cannot be zero.")

    # Initialize variables for the Extended Euclidean Algorithm
    x0, x1 = '1', '0'
    y0, y1 = '0', '1'
    a, b = x, m

    while b != '0':
        q = floor_div(a, b, base)
        r = modulus(a, b, base)

        a, b = b, r

        x0, x1 = x1, substraction(x0, multiplication(q, x1, base), base)
        y0, y1 = y1, substraction(y0, multiplication(q, y1, base), base)

    if a != '1':
        return 'ERROR - inverse does not exist'

    if x0[0] == '-':
        x0 = add(x0, m, base)

    return x0