def display_even_numbers_basic(numbers):
    """
    Displays even numbers from the list without using built-in functions.
    Uses manual loops and conditionals instead.
    """
    print("Even numbers: ", end="")
    has_even = False
    
    i = 0
    while i < len(numbers):
        if numbers[i] % 2 == 0:
            print(numbers[i], end=" ")
            has_even = True
        i = i + 1
    
    if not has_even:
        print("No even numbers found")
    else:
        print()


def get_even_numbers_basic(numbers):
    """
    Returns a list of even numbers without using built-in functions like list comprehension.
    """
    result = []
    i = 0
    
    while i < len(numbers):
        if numbers[i] % 2 == 0:
            result.append(numbers[i])
        i = i + 1
    
    return result


# Main program
if __name__ == "__main__":
    print("=== Program to Display Even Numbers (Without Built-in Functions) ===\n")
    
    # Test case 1: Mixed numbers
    test1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"Input: {test1}")
    display_even_numbers_basic(test1)
    
    # Test case 2: With negative numbers
    test2 = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4]
    print(f"\nInput: {test2}")
    display_even_numbers_basic(test2)
    
    # Test case 3: Empty list
    test3 = []
    print(f"\nInput: {test3}")
    display_even_numbers_basic(test3)
    
    # Test case 4: No even numbers
    test4 = [1, 3, 5, 7, 9]
    print(f"\nInput: {test4}")
    display_even_numbers_basic(test4)
    
    # Test case 5: Get even numbers as a list
    test5 = [10, 15, 20, 25, 30]
    print(f"\nInput: {test5}")
    even_result = get_even_numbers_basic(test5)
    print(f"Even numbers list: {even_result}")
