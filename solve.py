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
# Nam Mai (1959190)
# author_name_4 (author_student_ID_4)
##

# Import built-in json library for handling input/output 
import json
#import fixedint
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
    Converts a decimal (base-10) number to the target base (between 2 and 16) 
    without converting the number to an integer type.
    
    Parameters:
    number (str): The decimal number as a string.
    base (int): The base to convert to (between 2 and 16).
    
    Returns:
    str: The number in the target base as a string.
    """
    if base < 2 or base > 16:
        raise ValueError("Base must be between 2 and 16 (inclusive).")
    
    digits = "0123456789ABCDEF"
    
    # Check for negative number
    is_negative = number.startswith('-')
    if is_negative:
        number = number[1:]

    # Handle zero case
    if number == "0":
        return "0"
    
    result = ""
    
    # While the number is greater than 0
    while number != "0":
        # Calculate the remainder
        remainder = str(int(number) % base)  # Convert to int only for modulus
        result = digits[int(remainder)] + result
        
        # Perform floor division and update the number
        quotient = ""
        temp = 0
        for char in number:
            temp = temp * 10 + int(char)
            if temp >= base:
                quotient += str(temp // base)
                temp = temp % base
            elif quotient:  # avoid leading zeros
                quotient += '0'
        
        number = quotient if quotient else "0"

    return "-" + result if is_negative else result

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
            x = exercise["x"]
            y = exercise["y"]
            base = int(radix)
            answer["answer"] = helper.add(x,y,base)
            # Solve integer arithmetic addition exercise
        elif exercise["operation"] == "subtraction":
            # Solve integer arithmetic subtraction exercise
            x = exercise["x"]
            y = exercise["y"]
            base = int(radix)
            answer["answer"] = helper.subtractx(x,y,base)

        elif exercise["operation"] == "multiplication_primary":
            x = exercise["x"]
            y = exercise["y"]
            # Solve integer arithmetic multiplication by primary school method
            x = helper.convert_to_base_10(exercise["x"], exercise["radix"]) # convert x in radix given in the exercise to base 10
            y = helper.convert_to_base_10(exercise["y"], exercise["radix"]) # convert y in radix given in the exercise to base 10
            
            # Check the negativity of the result
            if x.startswith("-") ^ y.startswith("-"):
                isNegative = True
            
            # Take absolute values for multiplication
            int_x = abs(int(x))
            int_y = abs(int(y))
            
            # Convert numbers to strings
            x_str = str(int_x)
            y_str = str(int_y)
            
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
                
            answer["answer"] = convert_from_base_10(result_str, radix)
            
        elif exercise["operation"] == "multiplication_karatsuba":
            # Solve integer arithmetic multiplication by Karatsuba method
            x = helper.convert_to_base_10(exercise["x"], exercise["radix"]) # convert x in radix given in the exercise to base 10
            y = helper.convert_to_base_10(exercise["y"], exercise["radix"]) # convert y in radix given in the exercise to base 10
            # Check the negativity of the result
            if x.startswith("-") ^ y.startswith("-"):
                isNegative = True           
            # Get the absolute values
            int_x = abs(int(x))
            int_y = abs(int(y))
            # Base case for recursion: if either x or y is a single digit number
            if int_x < 10 or int_y < 10:
                answer = int_x * int_y
            # Convert numbers to strings
            x_str = str(x)
            y_str = str(y)
            # Calculates the size of the numbers
            maxSize = max(len(x_str), len(y_str))
            halfSize = maxSize // 2

            # Split x and y into two halves
            highX, lowX = int_x // (10**halfSize), int_x % (10**halfSize)
            highY, lowY = int_y // (10**halfSize), int_y % (10**halfSize)

            # Recursive calls for the three products
            firstPart = highX * highY                    
            middlePart = (highX + lowX) * (highY + lowY)
            lastPart = lowX * lowY                       

            # Karatsuba's formula to combine the products
            result = (firstPart * 10**(2 * halfSize)) + ((middlePart - firstPart - lastPart) * 10**halfSize) + lastPart
            result_str = str(result)
            # Apply the negative sign if needed
            if isNegative:
                result_str = '-' + result_str
                
            answer["answer"] = convert_from_base_10(result_str, radix)
            pass
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
            x = exercise["x"]
            modulus = exercise["modulus"]
            base = int(radix)
            # Keep reducing x until it is smaller than the modulus
            
            answer["answer"] = helper.modulus_red(x,modulus,radix)

            # x = helper.convert_to_base_10(exercise["x"], radix)
            # if exercise["modulus"].startswith("-"):
            #     modulus = helper.convert_to_base_10(exercise["modulus"][1:], radix)
            # else:
            #     modulus = helper.convert_to_base_10(exercise["modulus"], radix)

            # if modulus == "0":
            #     answer["answer"] = None
            # else:
            #     while x > modulus:
            #         sum = helper.substraction(x, modulus, 10)
            #     answer["answer"] = convert_from_base_10(x, radix)
        
        elif exercise["operation"] == "addition":
            # Solve modular arithmetic addition exercise
            # Convert x, y, m to base 10
            #x = helper.add(exercise["x"],exercise["y"], radix)
            #y = helper.convert_to_base_10(exercise["y"], radix)
            #modulus = helper.convert_to_base_10(exercise["modulus"], radix)
            x = exercise["x"]
            y = exercise["y"]

           
            modulus = exercise["modulus"]
            answer = helper.modulus_add(x,y,modulus,radix)

            
        
        elif exercise["operation"] == "subtraction":
            # Solve modular arithmetic subtraction exercise
            x = exercise["x"]
            y = exercise["y"]

           
            modulus = exercise["modulus"]
            answer = helper.modulus_substract(x,y,modulus,radix)



            
            
        
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
            raise ValueError(f"Unsupported operation: {exercise['operation']}")
    
    # Open file at answer_location for writing, creating the file if it does not exist yet
    # (and overwriting it if it does already exist).
    with open(answer_location, "w") as answer_file:
        # Serialize Python answer data (stored in answer) to JSON answer data and write it to answer_file
        json.dump(answer, answer_file, indent=4)

solve_exercise("Exercises/exercise3.json", "answer.json")
