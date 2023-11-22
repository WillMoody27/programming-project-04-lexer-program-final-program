import WHMLexer

# Student: William Hellems-Moody
# Date: 9/28/2023 (Updated: 11/21/23)
# Programming Project
# Class: CS 3210


'''
#  NOTE: OLD CODE FOR Manual Testing (Wasn't specified to use in Programming Project 03 instructions)
#       - If you want to run multiple expressions, uncomment this code below and run the program and manually input expressions

while True:
    text = input("WHM > ")
    # run the lexer program that takes in file name and text
    result, error = WHMLexer.run("<stdin>", text)
    if error:
        print(error.as_string())
    else:
        print(result)
'''


# Uncomment this section to run the test cases for Programming Project 03 and 04

# NOTE: To run all the test cases, uncomment the code below and run the program (This will work for WHMLexer.py)
# ****************************
# ADDED CODE FOR PROGRAM 03
# ****************************
# ********************
# Test Function for Program 03 - Testing multiple expressions (as requested in Programming Project 03 instructions)
# ********************
def Test(expression):
    result, error = WHMLexer.run("<test>", expression)
    if error:
        print(f"{error}\n")
    else:
        print(f"{result}\n")


if __name__ == "__main__":
    test_expressions = [
        "1 + 2 + 3 + 4",
        "1*2*3*4",
        "1-2-3-4",
        "1/2/3/4",
        "1*2+3*4",
        "1+2*3+4",
        "(1+2)*(3+4)",
        "1+(2*3)*(4+5)",
        "1+(2*3)/4+5",
        "5/(4+3)/2",
        "1 + 2.5",
        "125",
        "-1",
        "-1+(-2)",
        "-1+(-2.0)",
        "   1*2,5",
        "   1*2.5e2",
        "M1 + 2.5",
        "1 + 2&5",
        "1 * 2.5.6",
        "1 ** 2.5",
        "*1 / 2.5",
        # **** New test cases for Programming Project 04 Below ****
        "4 == 4",
        "4 == 5",
        "1 AND 0",
        "1 AND 1",
        "0 OR 1",
        "0 OR 0",
        "NOT 1",
        "NOT 0",
        "NOT (1 AND 0) OR (3 == 3)",
        "(2 == 2) AND (3 == 3)",
        "(2 == 3) OR (3 == 3)",
        "NOT((1 == 2) OR !(0 AND 1))",
        "NOT((1 OR 0) AND 0)",
        "NOT 0 AND 1",
        "1 + 2 * 3",
        "1 + * 3",
        # **** New test cases for Programming Project 04 Below ****
        # Check for ">=<=,<,>, AND, OR, NOT" operators - Program 04
        # General Comparison
        "5 > 3", # True
        "2 < 3", # True
        "7 <= 7", # True 
        "8 >= 10", # False 
        # Comparison with Arithmetic
        "(4 + 2) >= (3 * 2)", # True
        "(5 - 2) <= (8 / 4)", # False
        "4 * 2 < 5 * 2", # True
        # Nested Comparisons with Parentheses
        "(2 * (3 + 2)) >= (4 * 3)", # False
        "((6 / 2) - 1) < (2 + 2)", # True
        # Logical AND and OR with Comparisons
        "(3 > 2) AND (4 < 5)", # True
        "(5 >= 5) AND (1 + 1 < 2)", # False
        "(7 <= 7) OR (2 * 2 > 5)", # True
        "(4 + 3 > 7) OR (2 * 2 < 4)", # False
        # Complex Expressions
        "(5 >= 3) AND ((2 * 2) > (3 - 1))", # True
        "((3 + 2) >= 5) AND (2 < (5 - 2))", # True
        "(10 / 2 <= 3) OR (8 - 4 < 2)", # False
        # Check for NOT operator - Program 04
        "NOT 1", # False
        "not 1", # False
        "NOT 0", # True
        "NOT (1 AND 0)", # True
        # Check for != operator - Program 04
        "1 != 2", # True
        "1 != 1", # False
        "(4>2) AND (5==5)",
        # **** New test cases for Programming Project 04 Below ****
        # Five Test Cases for Program 04 for documentation
        "4 * (7 + 3) / 4",
        "NOT (1 AND 0) OR (3 == 3)",
        "(5 > 3) AND (2 <= 2)",
        "10 / (5 - 5)",
        "4 + -3",
    ]

    for expr in test_expressions:
        Test(expr)

    # End of code for Programming Project 03 and 04
        