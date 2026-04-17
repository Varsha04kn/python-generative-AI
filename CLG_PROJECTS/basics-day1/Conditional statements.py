#Conditional statements- if, if-else,nested, elif,
#if statement- used to execute a block of code if a specified condition is true
num = 10
if num %2 == 0:
    print(f"{num} is an even number.") 
print("----------------------------------")
#if else statement- used to execute a block of code if a specified condition is true, and another block of code if the condition is false

#elseif statement- used to execute a block of code if the condition in the if statement is false and another condition is true
num = 15
if num % 2 == 0:
    print(f"{num} is an even number.")
else:
    print(f"{num} is an odd number.")
print("----------------------------------")


#nested if else statement
a= 152
b= 19
c= 189
if a > b:
    if a > c:
        print(f"{a} is the greatest number.")
    else:
        print(f"{c} is the greatest number.")
else:
    if b > c:
        print(f"{b} is the greatest number.")
    else:
        print(f"{c} is the greatest number.")

print("----------------------------------")

#elif statement- used to execute a block of code if the condition in the if statement is false and another condition is true
num = 25
if num < 0:
    print(f"{num} is a negative number.")   
elif num == 0:
    print(f"{num} is zero.")
else:
    print(f"{num} is a positive number.")