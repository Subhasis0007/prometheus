# Task: Write a Python script that checks if the word 'kayak' is a palindrome.

## Verified Implementation
```python
def is_palindrome(s):
    """
    Check if the given string is a palindrome.
    
    :param s: String to check
    :return: True if the string is a palindrome, False otherwise
    """
    return s == s[::-1]

# Test the function with the word 'kayak'
word = 'kayak'
result = is_palindrome(word)

# Output the result
print(f"Is '{word}' a palindrome? {result}")
```
