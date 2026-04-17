from even_numbers import display_even_numbers
from even_numbers_sum import display_and_sum_even_numbers

display_even_numbers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])  # Prints: Even numbers: [2, 4, 6, 8, 10, 12]
          # Prints: No even numbers found in the list.
numbers = [1, 2, 3, 4, 5, 6]
total = display_and_sum_even_numbers(numbers)
print(f"Total sum of even numbers: {total}")
# Displays: Even numbers: 2 4 6 
# Returns: 12