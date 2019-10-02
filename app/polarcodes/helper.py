"""
Helper Functions for the polar codes
"""
import numpy as np


def is_power_of_2(number):
    return number != 0 and ((number & (number - 1)) == 0)


def div(a, b):
    """
    Simulates Matlab behaviour
    """

    if a == np.Inf and b == 0:
        return np.inf

    if a == 0 and b == 0:
        return np.nan

    if a > 0 and b == 0:
        return np.inf

    return a / b


def format_printing(to_print):
    print("\n\n ------------------------------------------------")
    print(" " + to_print)
    print(" ------------------------------------------------")
