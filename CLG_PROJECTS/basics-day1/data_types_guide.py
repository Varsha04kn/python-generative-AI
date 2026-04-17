"""
PRIMITIVE AND NON-PRIMITIVE DATA TYPES IN PYTHON
Complete guide with examples
"""

print("=" * 80)
print("PYTHON DATA TYPES: PRIMITIVE AND NON-PRIMITIVE")
print("=" * 80)

# ============================================================================
# PRIMITIVE DATA TYPES
# ============================================================================
print("\n" + "=" * 80)
print("PRIMITIVE DATA TYPES (Single Value)")
print("=" * 80)

# 1. INTEGER (int)
print("\n1. INTEGER (int)")
print("-" * 80)
age = 25
temperature = -10
year = 2024
print(f"Example 1: age = {age}, Type: {type(age)}")
print(f"Example 2: temperature = {temperature}, Type: {type(temperature)}")
print(f"Example 3: year = {year}, Type: {type(year)}")
print("Use Case: Storing whole numbers (age, count, quantity)")

# 2. FLOAT (float)
print("\n2. FLOAT (float)")
print("-" * 80)
height = 5.9
price = 99.99
pi = 3.14159
print(f"Example 1: height = {height}, Type: {type(height)}")
print(f"Example 2: price = {price}, Type: {type(price)}")
print(f"Example 3: pi = {pi}, Type: {type(pi)}")
print("Use Case: Storing decimal numbers (height, weight, price)")

# 3. STRING (str)
print("\n3. STRING (str)")
print("-" * 80)
name = "Alice"
city = 'New York'
message = "Hello World"
print(f"Example 1: name = '{name}', Type: {type(name)}")
print(f"Example 2: city = '{city}', Type: {type(city)}")
print(f"Example 3: message = '{message}', Type: {type(message)}")
print("Use Case: Storing text and characters (name, address, message)")

# 4. BOOLEAN (bool)
print("\n4. BOOLEAN (bool)")
print("-" * 80)
is_student = True
is_married = False
is_active = True
print(f"Example 1: is_student = {is_student}, Type: {type(is_student)}")
print(f"Example 2: is_married = {is_married}, Type: {type(is_married)}")
print(f"Example 3: is_active = {is_active}, Type: {type(is_active)}")
print("Use Case: Storing true/false values (yes/no, on/off)")

# ============================================================================
# NON-PRIMITIVE DATA TYPES
# ============================================================================
print("\n" + "=" * 80)
print("NON-PRIMITIVE DATA TYPES (Multiple Values)")
print("=" * 80)

# 1. LIST
print("\n1. LIST [ ]")
print("-" * 80)
fruits = ["Apple", "Banana", "Orange", "Mango"]
numbers = [1, 2, 3, 4, 5]
mixed = [10, "Hello", 3.14, True]
print(f"Example 1: fruits = {fruits}")
print(f"           Type: {type(fruits)}")
print(f"Example 2: numbers = {numbers}")
print(f"           Type: {type(numbers)}")
print(f"Example 3: mixed = {mixed}")
print(f"           Type: {type(mixed)}")
print("Characteristics: Ordered, Mutable, Allows Duplicates")
print("Use Case: Storing multiple items in a sequence")

# 2. TUPLE
print("\n2. TUPLE ( )")
print("-" * 80)
coordinates = (10, 20, 30)
colors = ("Red", "Green", "Blue")
mixed_tuple = (100, "Python", 3.14)
print(f"Example 1: coordinates = {coordinates}")
print(f"           Type: {type(coordinates)}")
print(f"Example 2: colors = {colors}")
print(f"           Type: {type(colors)}")
print(f"Example 3: mixed_tuple = {mixed_tuple}")
print(f"           Type: {type(mixed_tuple)}")
print("Characteristics: Ordered, Immutable, Allows Duplicates")
print("Use Case: Storing fixed/unchangeable collections")

# 3. SET
print("\n3. SET { }")
print("-" * 80)
unique_numbers = {1, 2, 3, 4, 5}
languages = {"Python", "Java", "C++", "JavaScript"}
numbers_with_duplicates = {1, 2, 2, 3, 3, 3, 4}
print(f"Example 1: unique_numbers = {unique_numbers}")
print(f"           Type: {type(unique_numbers)}")
print(f"Example 2: languages = {languages}")
print(f"           Type: {type(languages)}")
print(f"Example 3: numbers_with_duplicates = {numbers_with_duplicates}")
print(f"           (Duplicates removed automatically)")
print("Characteristics: Unordered, Mutable, No Duplicates")
print("Use Case: Storing unique values")

# 4. DICTIONARY
print("\n4. DICTIONARY { key: value }")
print("-" * 80)
student = {"name": "John", "age": 20, "grade": "A"}
person = {"first_name": "Alice", "last_name": "Johnson", "email": "alice@example.com"}
mixed_dict = {"id": 1, "name": "Bob", "score": 95.5, "is_active": True}
print(f"Example 1: student = {student}")
print(f"           Type: {type(student)}")
print(f"Example 2: person = {person}")
print(f"           Type: {type(person)}")
print(f"Example 3: mixed_dict = {mixed_dict}")
print(f"           Type: {type(mixed_dict)}")
print("Characteristics: Key-Value Pairs, Mutable, Ordered (Python 3.7+)")
print("Use Case: Storing data with meaningful keys")

# ============================================================================
# SUMMARY TABLE
# ============================================================================
print("\n" + "=" * 80)
print("QUICK REFERENCE TABLE")
print("=" * 80)

print("""
PRIMITIVE DATA TYPES:
┌─────────────┬──────────────────────────────────┬─────────────────┐
│ Type        │ Description                      │ Example         │
├─────────────┼──────────────────────────────────┼─────────────────┤
│ int         │ Whole numbers                    │ age = 25        │
│ float       │ Decimal numbers                  │ price = 99.99   │
│ str         │ Text/characters                  │ name = "Alice"  │
│ bool        │ True or False values             │ active = True   │
└─────────────┴──────────────────────────────────┴─────────────────┘

NON-PRIMITIVE DATA TYPES:
┌─────────────┬──────────────────────────────────┬──────────────────────────┐
│ Type        │ Characteristics                  │ Example                  │
├─────────────┼──────────────────────────────────┼──────────────────────────┤
│ list        │ Ordered, Mutable, Duplicates OK  │ [1, 2, 3, "hello"]       │
│ tuple       │ Ordered, Immutable, Duplicates   │ (1, 2, 3, "hello")       │
│ set         │ Unordered, Mutable, No Dups      │ {1, 2, 3, 4, 5}          │
│ dict        │ Key-Value, Mutable, Ordered      │ {"name": "John", "age":20}
└─────────────┴──────────────────────────────────┴──────────────────────────┘
""")

# ============================================================================
# ACCESSING ELEMENTS
# ============================================================================
print("\n" + "=" * 80)
print("ACCESSING ELEMENTS")
print("=" * 80)

fruits_list = ["Apple", "Banana", "Orange"]
colors_tuple = ("Red", "Green", "Blue")
unique_set = {10, 20, 30}
student_dict = {"name": "John", "age": 20}

print(f"\nLIST Access: fruits_list = {fruits_list}")
print(f"  First element: fruits_list[0] = {fruits_list[0]}")
print(f"  Last element: fruits_list[-1] = {fruits_list[-1]}")

print(f"\nTUPLE Access: colors_tuple = {colors_tuple}")
print(f"  First element: colors_tuple[0] = {colors_tuple[0]}")
print(f"  Last element: colors_tuple[-1] = {colors_tuple[-1]}")

print(f"\nDICTIONARY Access: student_dict = {student_dict}")
print(f"  By key: student_dict['name'] = {student_dict['name']}")
print(f"  By key: student_dict['age'] = {student_dict['age']}")

print("\nSET: Cannot access by index (unordered collection)")

# ============================================================================
# MODIFYING ELEMENTS
# ============================================================================
print("\n" + "=" * 80)
print("MODIFYING ELEMENTS")
print("=" * 80)

print("\nLIST (Mutable - Can modify):")
my_list = [1, 2, 3]
print(f"  Original: {my_list}")
my_list[0] = 99
print(f"  After change: {my_list}")

print("\nTUPLE (Immutable - Cannot modify):")
my_tuple = (1, 2, 3)
print(f"  Original: {my_tuple}")
try:
    my_tuple[0] = 99
except TypeError as e:
    print(f"  Error: Cannot modify tuple - {e}")

print("\nDICTIONARY (Mutable - Can modify):")
my_dict = {"x": 10, "y": 20}
print(f"  Original: {my_dict}")
my_dict["x"] = 99
print(f"  After change: {my_dict}")

print("\nSET (Mutable - Can add/remove):")
my_set = {1, 2, 3}
print(f"  Original: {my_set}")
my_set.add(4)
print(f"  After add: {my_set}")

print("\n" + "=" * 80)
print("END OF DATA TYPES GUIDE")
print("=" * 80)
