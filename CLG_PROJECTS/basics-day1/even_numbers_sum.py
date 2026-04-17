def display_and_sum_even_numbers(numbers):
    """
    Displays the even numbers from the list and returns their sum.
    Uses basic loops without built-in functions.
    
    Args:
        numbers: A list of numbers
    
    Returns:
        The sum of all even numbers in the list
    """
    even_sum = 0
    print("Even numbers: ", end="")
    has_even = False
    
    i = 0
    while i < len(numbers):
        if numbers[i] % 2 == 0:
            print(numbers[i], end=" ")
            even_sum = even_sum + numbers[i]
            has_even = True
        i = i + 1
    
    if not has_even:
        print("No even numbers found")
    else:
        print()
    
    return even_sum


def get_and_sum_even_numbers(numbers):
    """
    Returns a list of even numbers and their sum.
    """
    even_list = []
    even_sum = 0
    i = 0
    
    while i < len(numbers):
        if numbers[i] % 2 == 0:
            even_list.append(numbers[i])
            even_sum = even_sum + numbers[i]
        i = i + 1
    
    return even_list, even_sum


# Main program
if __name__ == "__main__":
    print("=== Program to Display Even Numbers and Calculate Their Sum ===\n")
    
    # Test case 1: Mixed numbers
    test1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"Input: {test1}")
    sum1 = display_and_sum_even_numbers(test1)
    print(f"Sum of even numbers: {sum1}")
    
    # Test case 2: With negative numbers
    test2 = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4]
    print(f"\nInput: {test2}")
    sum2 = display_and_sum_even_numbers(test2)
    print(f"Sum of even numbers: {sum2}")
    
    # Test case 3: Empty list
    test3 = []
    print(f"\nInput: {test3}")
    sum3 = display_and_sum_even_numbers(test3)
    print(f"Sum of even numbers: {sum3}")
    
    # Test case 4: No even numbers
    test4 = [1, 3, 5, 7, 9]
    print(f"\nInput: {test4}")
    sum4 = display_and_sum_even_numbers(test4)
    print(f"Sum of even numbers: {sum4}")
    
    # Test case 5: Using get_and_sum_even_numbers
    test5 = [10, 15, 20, 25, 30]
    print(f"\nInput: {test5}")
    even_list, total = get_and_sum_even_numbers(test5)
    print(f"Even numbers list: {even_list}")
    print(f"Sum of even numbers: {total}")
    
    # Test case 6: Larger numbers
    test6 = [100, 101, 102, 103, 104, 105]
    print(f"\nInput: {test6}")
    sum6 = display_and_sum_even_numbers(test6)
    print(f"Sum of even numbers: {sum6}")
