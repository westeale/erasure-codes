"""
Helper Functions for the polar codes
"""


def is_power_of_2(number):
    return number != 0 and ((number & (number - 1)) == 0)

def format_printing(to_print):
    print("\n\n ------------------------------------------------")
    print(" " + to_print)
    print(" ------------------------------------------------")
