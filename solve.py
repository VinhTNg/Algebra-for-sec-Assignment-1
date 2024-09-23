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

# Define a 32-bit integer type using fixedint
Int32 = fixedint.Int32

# Define the Int32 class
class Int32:
    def __init__(self, value):
        self.value = value & 0xFFFFFFFF  # Ensure it's a 32-bit integer

    def __int__(self):
        return self.value

def convert_to_base_10(number: str, base: int) -> int:
    """
    Manually converts a number in a given base to base 10 (decimal).

    Parameters:
    number (str): The number in the given base as a string.
    base (int): The base of the input number (between 2 and 16).

    Returns:
    int: The number converted to base 10.
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
    
    return -result if is_negative else result

def convert_from_base_10(number: int, base: int) -> str:
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
    
    if number == 0:
        return "0"
    
    is_negative = False
    if number < 0:
        is_negative = True
        number = -number
    
    result = ""
    while number > 0:
        remainder = number % base
        result = digits[remainder] + result
        number = number // base
    
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
            # Solve integer arithmetic addition exercise
            pass
        elif exercise["operation"] == "subtraction":
            # Solve integer arithmetic subtraction exercise
            pass
        # et cetera
    else:  # exercise["type"] == "modular_arithmetic"
        # Check what operation within the modular arithmetic operations we need to solve
        if exercise["operation"] == "reduction":
            # Solve modular arithmetic reduction exercise
            x = convert_to_base_10(exercise["x"], radix)
            modulus = convert_to_base_10(exercise["modulus"], radix)

            if modulus == 0:
                answer["answer"] = None
            else:
                # Convert to 32-bit integer
                x_32 = Int32(x)
                modulus_32 = Int32(modulus)
                reduction_result = Int32(x_32.int % modulus_32.int).int
                answer["answer"] = convert_from_base_10(reduction_result, radix)
        
        elif exercise["operation"] == "addition":
            # Solve modular arithmetic addition exercise
            # Convert x, y, m to base 10
            x = convert_to_base_10(exercise["x"], radix)
            y = convert_to_base_10(exercise["y"], radix)
            modulus = convert_to_base_10(exercise["modulus"], radix)
            
            if modulus == 0:
                answer["answer"] = None
            else:
                # Convert to 32-bit integers
                x_32 = Int32(x)
                y_32 = Int32(y)
                modulus_32 = Int32(modulus)
                addition_result = Int32((x_32.int + y_32.int) % modulus_32.int).int
                answer["answer"] = convert_from_base_10(addition_result, radix)
        
        elif exercise["operation"] == "subtraction":
            # Solve modular arithmetic subtraction exercise
            x = convert_to_base_10(exercise["x"], radix)
            y = convert_to_base_10(exercise["y"], radix)
            modulus = convert_to_base_10(exercise["modulus"], radix)
            
            if modulus == 0:
                answer["answer"] = None
            else:
                x_32 = Int32(x)
                y_32 = Int32(y)
                modulus_32 = Int32(modulus)
                subtraction_result = Int32((int(x_32) - int(y_32)) % int(modulus_32)).value
                # subtraction_result = modular_subtraction(x, y, modulus)
                if subtraction_result is None:
                    answer["answer"] = None
                else:
                    answer["answer"] = convert_from_base_10(subtraction_result, radix)
        
        elif exercise["operation"] == "multiplication":
            # Solve modular arithmetic multiplication exercise
            x = convert_to_base_10(exercise["x"], radix)
            y = convert_to_base_10(exercise["y"], radix)
            modulus = convert_to_base_10(exercise["modulus"], radix)
            
            if modulus == 0:
                answer["answer"] = None
            else:
                x_32 = Int32(x)
                y_32 = Int32(y)
                modulus_32 = Int32(modulus)
                multiplication_result = Int32((int(x_32) * int(y_32)) % int(modulus_32)).value
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

solve_exercise("SimpleExercises/exercise9.json", "answer.json")