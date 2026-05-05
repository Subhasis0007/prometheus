def is_prime(n: int) -> bool:
    """
    Check if the given number is a prime number.

    :param n: The number to check.
    :return: True if the number is prime, False otherwise.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def check_prime_generated_number(n: int) -> None:
    """
    Check if the given number is a prime number and print the result.

    :param n: The number to check.
    :return: None
    """
    if is_prime(n):
        print(f"{n} is a prime number.")
    else:
        print(f"{n} is not a prime number.")

def add_to_prime_list(n: int, prime_list: list) -> None:
    """
    Check if the given number is a prime number and add it to the list if it is.

    :param n: The number to check.
    :param prime_list: The list to add the prime number to.
    :return: None
    """
    if is_prime(n):
        prime_list.append(n)
        print(f"{n} is a prime number and added to the list.")
    else:
        print(f"{n} is not a prime number.")

def find_prime_numbers(count: int) -> list:
    """
    Find the specified number of prime numbers and return them in a list.

    :param count: The number of prime numbers to find.
    :return: A list of prime numbers.
    """
    prime_list = []
    num = 2
    while len(prime_list) < count:
        if is_prime(num):
            prime_list.append(num)
            print(f"{num} is a prime number and added to the list.")
        num += 1
    return prime_list

def calculate_average_of_primes(count: int) -> float:
    """
    Find the specified number of prime numbers, calculate their average, and return it.

    :param count: The number of prime numbers to find and calculate the average.
    :return: The average of the prime numbers.
    """
    prime_list = find_prime_numbers(count)
    if not prime_list:
        return 0.0
    return sum(prime_list) / len(prime_list)

def print_prime_numbers_and_average(count: int) -> None:
    """
    Find the specified number of prime numbers, print the list, and calculate their average.

    :param count: The number of prime numbers to find, print, and calculate the average.
    :return: None
    """
    prime_list = find_prime_numbers(count)
    print("List of prime numbers:", prime_list)
    if prime_list:
        average = calculate_average_of_primes(count)
        print(f"The average of the first {count} prime numbers is: {average}")
    else:
        print("No prime numbers found.")

# Example usage
print_prime_numbers_and_average(10)