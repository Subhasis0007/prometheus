import argparse

def check_even_odd(number: int) -> str:
    """
    Takes an integer and returns 'even' if the number is even, 'odd' otherwise.

    :param number: Integer to check
    :return: String 'even' or 'odd'
    """
    if number % 2 == 0:
        return "even"
    else:
        return "odd"

def main():
    """
    Main script that parses command-line arguments and checks if the number is even or odd.
    """
    parser = argparse.ArgumentParser(description="Check if a number is even or odd.")
    parser.add_argument("number", type=int, help="The number to check")
    args = parser.parse_args()

    try:
        number_to_check = int(args.number)
    except ValueError:
        print("Error: The provided argument is not a valid integer.")
        return

    try:
        result = check_even_odd(number_to_check)
    except Exception as e:
        print(f"Error: {e}")
        return

    print(f"The number {number_to_check} is {result}.")

if __name__ == "__main__":
    main()