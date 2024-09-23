symbols: list[str] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

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
    # Handle negative cases
    if x[0] == '-' and y[0] == '-':
        return make_neg(addition(make_neg(x), make_neg(y), base))
    if x[0] == '-':
        return substraction(y, make_neg(x), base)
    if y[0] == '-':
        return substraction(x, make_neg(y), base)

    max_len = max(len(x), len(y))
    x, y = x.zfill(max_len), y.zfill(max_len)

    carry = 0
    result = ''

    for i in range(max_len - 1, -1, -1):
        total = carry + int(x[i], base) + int(y[i], base)
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
    # Handle cases with negatives
    if x[0] == '-' and y[0] == '-':
        return substraction(make_neg(y), make_neg(x), base)
    if x[0] == '-':
        return make_neg(addition(make_neg(x), y, base))
    if y[0] == '-':
        return addition(x, make_neg(y), base)

    if len(y) > len(x) or (len(x) == len(y) and is_greater(y, x, base)):
        return make_neg(substraction(y, x, base))

    max_len = max(len(x), len(y))
    x, y = x.zfill(max_len), y.zfill(max_len)

    carry = 0
    result = ''

    for i in range(max_len - 1, -1, -1):
        diff = int(x[i], base) - int(y[i], base) - carry
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
    if x[0] == '-' and y[0] == '-':
        return multiplication(make_neg(x), make_neg(y), base)
    if x[0] == '-':
        return make_neg(multiplication(make_neg(x), y, base))
    if y[0] == '-':
        return make_neg(multiplication(x, make_neg(y), base))

    max_len = max(len(x), len(y))
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
