

#non primitive data types - list, tuple, set, dict- can accept multiple values at a time
hobbies = ["reading", "traveling", "cooking","painting"]  # List of hobbies
print(hobbies, type(hobbies))  # Output: ['reading', 'traveling', 'cooking', 'painting'] <class 'list'>
#tuple- ordered, immutable, allows duplicates
languages = ("Python", "Java", "C++", "Python")  # Tuple of programming languages
print(languages, type(languages))  # Output: ('Python', 'Java', 'C++', 'Python') <class 'tuple'>
# set- unordered, mutable, no duplicates,only unique values
even_numbers = {2, 4, 6, 8, 10,}
print(even_numbers, type(even_numbers))  # Output: {2, 4, 6, 8, 10} <class 'set'>
dict_example = {"name": "varsha", "age": 18, "city": "bengaluru"}  # Dictionary with key-value pairs
print(dict_example, type(dict_example))  # Output: {'name': 'varsha', 'age': 18, 'city': 'bengaluru'} <class 'dict'> 