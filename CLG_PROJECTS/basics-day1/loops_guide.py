"""
PYTHON LOOPS - COMPREHENSIVE GUIDE WITH EXAMPLES
Includes: for loops, while loops, loop control statements, and nested loops
"""

print("=" * 80)
print("PYTHON LOOPS - COMPLETE GUIDE")
print("=" * 80)

# ============================================================================
# 1. FOR LOOP
# ============================================================================
print("\n" + "=" * 80)
print("1. FOR LOOP - Iterates over a sequence")
print("=" * 80)

# Example 1: For loop with range
print("\nExample 1: For loop with range()")
print("-" * 80)
print("Code: for i in range(1, 6):")
print("          print(i)")
print("\nOutput:")
for i in range(1, 6):
    print(i, end=" ")
print()

# Example 2: For loop with list
print("\nExample 2: For loop with list")
print("-" * 80)
fruits = ["Apple", "Banana", "Orange", "Mango"]
print(f"fruits = {fruits}")
print("\nCode: for fruit in fruits:")
print("          print(fruit)")
print("\nOutput:")
for fruit in fruits:
    print(fruit)

# Example 3: For loop with string
print("\nExample 3: For loop with string")
print("-" * 80)
word = "Python"
print(f"word = '{word}'")
print("\nCode: for char in word:")
print("          print(char, end=' ')")
print("\nOutput:")
for char in word:
    print(char, end=" ")
print()

# Example 4: For loop with range(start, stop, step)
print("\nExample 4: For loop with range(start, stop, step)")
print("-" * 80)
print("Code: for i in range(0, 10, 2):")
print("          print(i, end=' ')")
print("\nOutput:")
for i in range(0, 10, 2):
    print(i, end=" ")
print()

# Example 5: For loop with enumerate (index + value)
print("\nExample 5: For loop with enumerate (index + value)")
print("-" * 80)
colors = ["Red", "Green", "Blue"]
print(f"colors = {colors}")
print("\nCode: for index, color in enumerate(colors):")
print("          print(f'{index}: {color}')")
print("\nOutput:")
for index, color in enumerate(colors):
    print(f"{index}: {color}")

# Example 6: For loop with dictionary
print("\nExample 6: For loop with dictionary")
print("-" * 80)
student = {"name": "John", "age": 20, "grade": "A"}
print(f"student = {student}")
print("\nCode: for key, value in student.items():")
print("          print(f'{key}: {value}')")
print("\nOutput:")
for key, value in student.items():
    print(f"{key}: {value}")

# ============================================================================
# 2. WHILE LOOP
# ============================================================================
print("\n" + "=" * 80)
print("2. WHILE LOOP - Repeats as long as condition is true")
print("=" * 80)

# Example 1: Basic while loop
print("\nExample 1: Basic while loop")
print("-" * 80)
print("Code: i = 1")
print("      while i <= 5:")
print("          print(i, end=' ')")
print("          i = i + 1")
print("\nOutput:")
i = 1
while i <= 5:
    print(i, end=" ")
    i = i + 1
print()

# Example 2: While loop with user input simulation
print("\nExample 2: While loop - countdown")
print("-" * 80)
print("Code: count = 5")
print("      while count > 0:")
print("          print(count)")
print("          count = count - 1")
print("\nOutput:")
count = 5
while count > 0:
    print(count)
    count = count - 1

# Example 3: While loop with condition
print("\nExample 3: While loop - sum until condition")
print("-" * 80)
print("Code: number = 1")
print("      sum_value = 0")
print("      while number <= 5:")
print("          sum_value = sum_value + number")
print("          number = number + 1")
print("      print(f'Sum: {sum_value}')")
print("\nOutput:")
number = 1
sum_value = 0
while number <= 5:
    sum_value = sum_value + number
    number = number + 1
print(f"Sum: {sum_value}")

# ============================================================================
# 3. BREAK STATEMENT
# ============================================================================
print("\n" + "=" * 80)
print("3. BREAK STATEMENT - Exit the loop immediately")
print("=" * 80)

# Example 1: Break in for loop
print("\nExample 1: Break in for loop")
print("-" * 80)
print("Code: for i in range(1, 10):")
print("          if i == 5:")
print("              break")
print("          print(i, end=' ')")
print("\nOutput:")
for i in range(1, 10):
    if i == 5:
        break
    print(i, end=" ")
print()

# Example 2: Break in while loop
print("\nExample 2: Break in while loop - find number")
print("-" * 80)
numbers = [1, 3, 5, 7, 9, 4, 8]
print(f"numbers = {numbers}")
print("\nCode: for num in numbers:")
print("          if num == 4:")
print("              print('Found 4')")
print("              break")
print("          print(num, end=' ')")
print("\nOutput:")
for num in numbers:
    if num == 4:
        print("Found 4")
        break
    print(num, end=" ")
print()

# ============================================================================
# 4. CONTINUE STATEMENT
# ============================================================================
print("\n" + "=" * 80)
print("4. CONTINUE STATEMENT - Skip current iteration")
print("=" * 80)

# Example 1: Continue in for loop
print("\nExample 1: Continue in for loop (skip even numbers)")
print("-" * 80)
print("Code: for i in range(1, 8):")
print("          if i % 2 == 0:")
print("              continue")
print("          print(i, end=' ')")
print("\nOutput:")
for i in range(1, 8):
    if i % 2 == 0:
        continue
    print(i, end=" ")
print()

# Example 2: Continue in while loop
print("\nExample 2: Continue in while loop (skip zero)")
print("-" * 80)
print("Code: nums = [1, 0, 2, 0, 3, 4]")
print("      for num in nums:")
print("          if num == 0:")
print("              continue")
print("          print(num, end=' ')")
nums = [1, 0, 2, 0, 3, 4]
print("\nOutput:")
for num in nums:
    if num == 0:
        continue
    print(num, end=" ")
print()

# ============================================================================
# 5. NESTED LOOPS
# ============================================================================
print("\n" + "=" * 80)
print("5. NESTED LOOPS - Loop inside another loop")
print("=" * 80)

# Example 1: Nested for loops (multiplication table)
print("\nExample 1: Multiplication table (2x3)")
print("-" * 80)
print("Code: for i in range(1, 3):")
print("          for j in range(1, 4):")
print("              print(f'{i}x{j}={i*j}', end='  ')")
print("          print()")
print("\nOutput:")
for i in range(1, 3):
    for j in range(1, 4):
        print(f"{i}x{j}={i*j}", end="  ")
    print()

# Example 2: Pattern printing
print("\nExample 2: Pattern printing (triangle)")
print("-" * 80)
print("Code: for i in range(1, 5):")
print("          for j in range(i):")
print("              print('*', end=' ')")
print("          print()")
print("\nOutput:")
for i in range(1, 5):
    for j in range(i):
        print("*", end=" ")
    print()

# Example 3: Nested loops with lists
print("\nExample 3: Nested loops with lists")
print("-" * 80)
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(f"matrix = {matrix}")
print("\nCode: for row in matrix:")
print("          for num in row:")
print("              print(num, end=' ')")
print("          print()")
print("\nOutput:")
for row in matrix:
    for num in row:
        print(num, end=" ")
    print()

# ============================================================================
# 6. PASS STATEMENT
# ============================================================================
print("\n" + "=" * 80)
print("6. PASS STATEMENT - Placeholder (does nothing)")
print("=" * 80)

# Example 1: Pass in loop
print("\nExample 1: Pass statement in loop")
print("-" * 80)
print("Code: for i in range(3):")
print("          pass  # Placeholder - loop continues")
print("\nOutput: Loop runs but does nothing")
for i in range(3):
    pass

# ============================================================================
# 7. ELSE WITH LOOPS
# ============================================================================
print("\n" + "=" * 80)
print("7. ELSE WITH LOOPS - Executes if loop completes normally")
print("=" * 80)

# Example 1: For-else
print("\nExample 1: For-else (no break)")
print("-" * 80)
print("Code: for i in range(1, 4):")
print("          print(i, end=' ')")
print("      else:")
print("          print('Loop completed successfully')")
print("\nOutput:")
for i in range(1, 4):
    print(i, end=" ")
else:
    print("Loop completed successfully")

# Example 2: For-else with break
print("\nExample 2: For-else (with break - else NOT executed)")
print("-" * 80)
print("Code: for i in range(1, 10):")
print("          if i == 3:")
print("              print('Breaking...')")
print("              break")
print("      else:")
print("          print('Loop completed')")
print("\nOutput:")
for i in range(1, 10):
    if i == 3:
        print("Breaking...")
        break
else:
    print("Loop completed")

# ============================================================================
# 8. PRACTICAL EXAMPLES
# ============================================================================
print("\n" + "=" * 80)
print("8. PRACTICAL EXAMPLES")
print("=" * 80)

# Example 1: Sum of numbers
print("\nExample 1: Calculate sum of numbers 1 to 10")
print("-" * 80)
total = 0
for i in range(1, 11):
    total = total + i
print(f"Sum of 1 to 10: {total}")

# Example 2: Find maximum in list
print("\nExample 2: Find maximum number in list")
print("-" * 80)
numbers = [10, 5, 20, 15, 8]
max_num = numbers[0]
for num in numbers:
    if num > max_num:
        max_num = num
print(f"Numbers: {numbers}")
print(f"Maximum: {max_num}")

# Example 3: Count vowels in string
print("\nExample 3: Count vowels in string")
print("-" * 80)
text = "Hello World"
vowel_count = 0
vowels = "aeiouAEIOU"
for char in text:
    if char in vowels:
        vowel_count = vowel_count + 1
print(f"Text: '{text}'")
print(f"Vowel count: {vowel_count}")

# Example 4: Print times table
print("\nExample 4: Print times table of 5")
print("-" * 80)
number = 5
print(f"Times table of {number}:")
for i in range(1, 11):
    print(f"{number} x {i} = {number * i}")

print("\n" + "=" * 80)
print("END OF LOOPS GUIDE")
print("=" * 80)
