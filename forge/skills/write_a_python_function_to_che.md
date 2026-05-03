# Task: Write a python function to check if a string is a palindrome and test it on the word 'racecar'.

## Verified Implementation
```python
def is_palindrome(s):
    """
    Check if the given string is a palindrome.
    
    :param s: String to check
    :return: True if the string is a palindrome, False otherwise
    """
    return s == s[::-1]

# Test the function with the word 'racecar'
test_string = 'racecar'
result = is_palindrome(test_string)
print(f"The string '{test_string}' is a palindrome: {result}")
```
