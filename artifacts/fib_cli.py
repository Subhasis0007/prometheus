import sys


def validate_positive_integer(n: int) -> bool:
    """
    Validate if the given number is a positive integer.

    Args:
        n (int): The number to validate.

    Returns:
        bool: True if the number is a positive integer, False otherwise.
    """
    return isinstance(n, int) and n > 0


def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number.

    Args:
        n (int): The position in the Fibonacci sequence.

    Returns:
        int: The nth Fibonacci number.
    """
    if n <= 0:
        raise ValueError("The argument must be a positive integer.")
    elif n == 1:
        return 0
    elif n == 2:
        return 1

    a, b = 0, 1
    for _ in range(2, n):
        a, b = b, a + b
    return b


def main():
    """
    Main function to validate command-line argument and calculate the Fibonacci number.
    """
    if len(sys.argv) != 2:
        print("Usage: python script.py <positive_integer>")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        if not validate_positive_integer(n):
            print("Error: The argument must be a positive integer.")
            sys.exit(1)
    except ValueError:
        print("Error: The argument must be an integer.")
        sys.exit(1)

    result = fibonacci(n)
    print(result)


if __name__ == "__main__":
    main()