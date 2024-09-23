##
# 2WF90 Algebra for Security -- Software Assignment 1 
# Integer and Modular Arithmetic
# solve.py
#
#
# Group number:
# group_number 
#
# Author names and student IDs:
# Vinh Nguyen (1957104) 
# Khoi Nguyen (1979388)
# author_name_3 (author_student_ID_3)
# author_name_4 (author_student_ID_4)
##

# Import built-in json library for handling input/output 
import json
import fixedint
import helper

def gcdExtended(a: int, b: int) -> tuple[int, int, int]:
    # Base Case
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = gcdExtended(max(b,a) % min(b,a), min(b,a))

    # Update x and y using results of recursive
    # call
    x = y1 - (b//a) * x1
    y = x1

    return gcd, x, y

def convert_from_base_10(number: str, base: int) -> str:
    """
    Manually converts a decimal (base-10) number to the target base (between 2 and 16).
    
    Parameters:
    number (int): The decimal number to convert.
    base (int): The base to convert to (between 2 and 16).
    
    Returns:
    str: The number in the target base as a string.
    """
    if base < 2 or base > 16:
        raise ValueError("Base must be between 2 and 16 (inclusive).")
    
    digits = "0123456789ABCDEF"
    str_base = str(base)
    if number == "0":
        return "0"
    
    is_negative = False
    if number.startswith("-"):
        is_negative = True
        number = number[1:]
    
    result = ""
    while helper.is_greater(number, "0", 10):
        remainder = helper.mod(number, str_base, base)
        result = digits[int(remainder)] + result
        number = helper.floor_div(number, str_base, base)
    
    return "-" + result if is_negative else result

#test convert_from_base_10
print(convert_from_base_10("10", 2)) # 1010

def solve_exercise(exercise_location : str, answer_location : str):
    """
    Solves an exercise specified in the file located at exercise_location and
    writes the answer to a file at answer_location. Note: the file at
    answer_location might not exist yet and, hence, might still need to be created.
    """
    
    # Open file at exercise_location for reading.
    with open(exercise_location, "r") as exercise_file:
        # Deserialize JSON exercise data present in exercise_file to corresponding Python exercise data 
        exercise = json.load(exercise_file)
        
    ### Parse and solve ###

    # Initialize the answer dictionary to store the results
    answer = {}

    # Get the radix
    radix = exercise.get("radix")
    if radix is None:
        raise ValueError("Radix not specified in the exercise.")

    # Check type of exercise
    if exercise["type"] == "integer_arithmetic":
        # Check what operation within the integer arithmetic operations we need to solve
        if exercise["operation"] == "addition":
            x =exercise["x"]
            y = exercise["y"]
            base = int(radix)
            answer["answer"] = add(x,y,base)
            # Solve integer arithmetic addition exercise
            #pass
        elif exercise["operation"] == "subtraction":
            # Solve integer arithmetic subtraction exercise
            x = helper.convert_to_base_10(exercise["x"], radix)
            y = helper.convert_to_base_10(exercise["y"], radix)
            answer["answer"] = convert_from_base_10(x - y, radix)
        elif exercise["operation"] == "multiplication_primary":
            # Solve integer arithmetic multiplication by primary school method
            x = helper.convert_to_base_10(exercise["x"], exercise["radix"]) # convert x in radix given in the exercise to base 10
            y = helper.helper.convert_to_base_10(exercise["y"], exercise["radix"]) # convert y in radix given in the exercise to base 10
            
            # Check the negativity of the result
            isNegative = (x < 0) ^ (y < 0)  # XOR: True if only one of them is negative
            
            # Take absolute values for multiplication
            x = abs(x)
            y = abs(y)
            
            # Convert numbers to strings
            x_str = str(x)
            y_str = str(y)
            
            #Reverse both string 
            x_str = x_str[::-1]
            y_str = y_str[::-1]
            
            # Initialize a list to store the intermediate results
            results = [0] * (len(x_str) + len(y_str))
            
            # Perform the multiplication digit by digit
            for i in range(len(x_str)):
                for j in range(len(y_str)):
                    
                    # Multiply the digits and add to the corresponding position in results
                    multiSingleDigit = int(x_str[i]) * int(y_str[j])
                    results[i + j] += multiSingleDigit
            
                    # Handle carry if the result is more than 9
                    if results[i + j] >= 10:
                        results[i + j + 1] += results[i + j] // 10
                        results[i + j] %= 10
    
            # Remove leading zeros from the results
            while len(results) > 1 and results[-1] == 0:
                results.pop()
    
            # Convert the results list back into a number
            result_str = ''.join(map(str, results[::-1]))
            
            # Apply the negative sign if needed
            if isNegative:
                result_str = '-' + result_str
    
            answer["answer"] = convert_from_base_10(int(result_str), radix)
        elif exercise["operation"] == "multiplication_karatsuba":
            def Karatsuba(x, y):
                # Base case for recursion: if either x or y is a single digit number
                if x < 10 or y < 10:
                    answer = x * y
                # Check the negativity of the result
                isNegative = (x < 0) ^ (y < 0)  # XOR: True if only one of them is negative
                # Get the absolute values
                x = abs(x)
                y = abs(y)
                # Convert numbers to strings
                x_str = str(x)
                y_str = str(y)
                # Calculates the size of the numbers
                maxSize = max(len(x_str), len(y_str))
                halfSize = maxSize // 2

                # Split x and y into two halves
                highX, lowX = x // (10**halfSize), x % (10**halfSize)
                highY, lowY = y // (10**halfSize), y % (10**halfSize)

                # Recursive calls for the three products
                firstPart = Karatsuba(highX, highY)                     # highX * highY
                middlePart = Karatsuba((highX + lowX), (highY + lowY))  # (lowX + highX) * (lowY + highY)
                lastPart = Karatsuba(lowX, lowY)                        # lowX * lowY

                # Karatsuba's formula to combine the products
                result = (firstPart * 10**(2 * halfSize)) + ((middlePart - firstPart - lastPart) * 10**halfSize) + lastPart
                result_str = str(result)
                # Apply the negative sign if needed
                if isNegative:
                    result_str = '-' + result_str
                answer = int(result_str)
                return answer
                
            # Solve integer arithmetic multiplication by Karatsuba method
            x = helper.convert_to_base_10(exercise["x"], exercise["radix"]) # convert x in radix given in the exercise to base 10
            y = helper.convert_to_base_10(exercise["y"], exercise["radix"]) # convert y in radix given in the exercise to base 10
            
            answer["answer"] = convert_from_base_10(Karatsuba(x, y), radix)
        elif exercise["operation"] == "extended_euclidean_algorithm":
            x = helper.convert_to_base_10(exercise["x"], radix)
            y = helper.convert_to_base_10(exercise["y"], radix)
            gcd, a, b = gcdExtended(x, y)
            answer["answer-a"] = convert_from_base_10(a, radix)
            answer["answer-b"] = convert_from_base_10(b, radix)
            answer["answer-gcd"] = convert_from_base_10(gcd, radix)
    else:  # exercise["type"] == "modular_arithmetic"
        # Check what operation within the modular arithmetic operations we need to solve
        if exercise["operation"] == "reduction":
            # Solve modular arithmetic reduction exercise
            x = helper.convert_to_base_10(exercise["x"], radix)
            if exercise["modulus"].startswith("-"):
                modulus = helper.convert_to_base_10(exercise["modulus"][1:], radix)
            else:
                modulus = helper.convert_to_base_10(exercise["modulus"], radix)

            if modulus == "0":
                answer["answer"] = None
            else:
                while x > modulus:
                    sum = helper.substraction(x, modulus, 10)
                answer["answer"] = convert_from_base_10(x, radix)
        
        elif exercise["operation"] == "addition":
            # Solve modular arithmetic addition exercise
            # Convert x, y, m to base 10
            x = helper.convert_to_base_10(exercise["x"], radix)
            y = helper.convert_to_base_10(exercise["y"], radix)
            if exercise["modulus"].startswith("-"):
                modulus = helper.convert_to_base_10(exercise["modulus"][1:], radix)
            else:
                modulus = helper.convert_to_base_10(exercise["modulus"], radix)
            
            if modulus == "0":
                answer["answer"] = None
            else:
                sum = x + y
                while sum > modulus:
                    sum = helper.substraction(sum, modulus, 10)
                answer["answer"] = convert_from_base_10(sum, radix)
        
        elif exercise["operation"] == "subtraction":
            # Solve modular arithmetic subtraction exercise
            x = helper.convert_to_base_10(exercise["x"], radix)
            y = helper.convert_to_base_10(exercise["y"], radix)
            modulus = helper.convert_to_base_10(exercise["modulus"], radix)
            
            if modulus == 0:
                answer["answer"] = None
            else:
                subtraction_result = (x - y) % modulus
                # subtraction_result = modular_subtraction(x, y, modulus)
                if subtraction_result is None:
                    answer["answer"] = None
                else:
                    answer["answer"] = convert_from_base_10(subtraction_result, radix)
        
        elif exercise["operation"] == "multiplication":
            # Solve modular arithmetic multiplication exercise
            x = helper.convert_to_base_10(exercise["x"], radix)
            y = helper.convert_to_base_10(exercise["y"], radix)
            modulus = helper.convert_to_base_10(exercise["modulus"], radix)
            
            if modulus == 0:
                answer["answer"] = None
            else:
                multiplication_result = (x * y) % modulus
                if multiplication_result is None:
                    answer["answer"] = None
                else:
                    answer["answer"] = convert_from_base_10(multiplication_result, radix)
        
        elif exercise["operation"] == "inversion":
            # Implement modular inversion if needed
            # Placeholder for future implementation
            pass
        
        else:
            raise ValueError(f"Unsupported operation: {exercise["operation"]}")
    
    # Open file at answer_location for writing, creating the file if it does not exist yet
    # (and overwriting it if it does already exist).
    with open(answer_location, "w") as answer_file:
        # Serialize Python answer data (stored in answer) to JSON answer data and write it to answer_file
        json.dump(answer, answer_file, indent=4)

solve_exercise("Exercises/exercise4.json", "answer.json")
