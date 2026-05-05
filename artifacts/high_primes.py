def is_prime(n):
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

def find_primes_in_range(start, end):
    primes = []
    for num in range(start, end + 1):
        if is_prime(num):
            primes.append(num)
    return primes

def call_prime_check_for_each_number(start, end):
    for num in range(start, end + 1):
        if is_prime(num):
            print(f"{num} is a prime number.")
        else:
            print(f"{num} is not a prime number.")

primes_between_500_and_1000 = find_primes_in_range(500, 1000)
print("Prime numbers between 500 and 1000:", primes_between_500_and_1000)
call_prime_check_for_each_number(500, 1000)