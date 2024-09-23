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
# author_name_2 (author_student_ID_2)
# author_name_3 (author_student_ID_3)
# author_name_4 (author_student_ID_4)
##

# Import built-in json library for handling input/output 
import json

def convert_to_base_10(number: str, base: int) -> int:
    """
    Converts a number in a given base to base 10 (decimal).

    Parameters:
    number (str): The number in the given base as a string.
    base (int): The base of the input number (between 2 and 16).

    Returns:
    int: The number converted to base 10.
    """
    if base < 2 or base > 16:
        raise ValueError("Base must be between 2 and 16 (inclusive).")
    
    return int(number, base)

def convert_from_base_10(number: int, base: int) -> str:
    """
    Converts a decimal (base-10) number to the original base (between 2 and 16).
    
    Parameters:
    number (int): The decimal number to convert.
    base (int): The base to convert to (between 2 and 16).
    
    Returns:
    str: The number in the target base as a string.
    """
    if base < 2 or base > 16:
        raise ValueError("Base must be between 2 and 16 (inclusive).")
    
    if number == 0:
        return "0"

    digits = "0123456789ABCDEF"
    result = ""

    while number > 0:
        remainder = number % base
        result = digits[remainder] + result
        number = number // base

    return result

def solve_exercise(exercise_location : str, answer_location : str):
    """
    solves an exercise specified in the file located at exercise_location and
    writes the answer to a file at answer_location. Note: the file at
    answer_location might not exist yet and, hence, might still need to be created.
    """
    
    # Open file at exercise_location for reading.
    with open(exercise_location, "r") as exercise_file:
        # Deserialize JSON exercise data present in exercise_file to corresponding Python exercise data 
        exercise = json.load(exercise_file)
        

    ### Parse and solve ###

    # Check type of exercise
    if exercise["type"] == "integer_arithmetic":
        # Check what operation within the integer arithmetic operations we need to solve
        if exercise["operation"] == "addition":
            # Solve integer arithmetic addition exercise
            x = convert_to_base_10(exercise["x"], exercise["radix"])
            y = convert_to_base_10(exercise["y"], exercise["radix"])
            answer = x + y
            answer = convert_from_base_10(answer, exercise["radix"])
        elif exercise["operation"] == "subtraction":
            # Solve integer arithmetic subtraction exercise
            x = convert_to_base_10(exercise["x"], exercise["radix"])
            y = convert_to_base_10(exercise["y"], exercise["radix"])
            answer = x - y
            answer = convert_from_base_10(answer, exercise["radix"])
        # et cetera
    else: # exercise["type"] == "modular_arithmetic"
        # Check what operation within the modular arithmetic operations we need to solve
        if exercise["operation"] == "reduction":
            # Solve modular arithmetic reduction exercise
            # Convert x, m to base 10
            x = convert_to_base_10(exercise["x"], exercise["radix"])
            modulus = convert_to_base_10(exercise["modulus"], exercise["radix"])
            # If modulus is 0, return null
            if(modulus == 0):
                answer = None
            else :
                # Calculate x mod m
                answer = x % modulus
                answer = convert_from_base_10(answer, exercise["radix"])
        elif exercise["operation"] == "addition":
            # Solve modular arithmetic addition exercise
            # Convert x, y, m to base 10
            x = convert_to_base_10(exercise["x"], exercise["radix"])
            y = convert_to_base_10(exercise["y"], exercise["radix"])
            modulus = convert_to_base_10(exercise["modulus"], exercise["radix"])
            # If modulus is 0, return null
            if(modulus == 0):
                answer = None
            else:
                # Calculate (x + y) mod m
                answer = (x + y) % modulus
                answer = convert_from_base_10(answer, exercise["radix"])
        


    # Open file at answer_location for writing, creating the file if it does not exist yet
    # (and overwriting it if it does already exist).
    with open(answer_location, "w") as answer_file:
        # Serialize Python answer data (stored in answer) to JSON answer data and write it to answer_file
        json.dump(answer, answer_file, indent=4)

if __name__ == "__main__":
    exercise_path = "Exercise/exercise4.json"  # Path to the exercise file
    answer_path = "Answer/answer4.json"        # Path to the output file
    
    solve_exercise(exercise_path, answer_path)

