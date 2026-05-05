def add_numbers(a: float, b: float) -> float:
    """
    Adds two numbers together.

    Parameters:
    a (float): The first number to add.
    b (float): The second number to add.

    Returns:
    float: The sum of a and b.
    """
    return a + b

# Example usage:
result = add_numbers(5.0, 3.0)
print(result)  # Output: 8.0

"""
This function adds two numbers together and returns the sum.
"""
add_numbers.__doc__ = """
    Adds two numbers together.

    Parameters:
    a (float): The first number to add.
    b (float): The second number to add.

    Returns:
    float: The sum of a and b.
    """
# Example usage:
result = add_numbers(5.0, 3.0)
print(result)  # Output: 8.0