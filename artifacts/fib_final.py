def fibonacci(n):
    """
    Compute the n-th Fibonacci number using an iterative approach.

    Parameters:
    n (int): The position in the Fibonacci sequence.

    Returns:
    int: The n-th Fibonacci number.
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

for i in range(20):
    print(f"Fibonacci({i}) = {fibonacci(i)}")