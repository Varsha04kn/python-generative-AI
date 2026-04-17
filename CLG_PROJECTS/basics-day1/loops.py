#loops-used to repeat a block of code multiple times
#while loop- used to repeat a block of code as long as a condition is true
count=1
while count <= 5:
    print(count)
    if count == 3:
        print("Count is 3, breaking the loop.")
        break  # Exit the loop when count is 3
    count += 1

#to print even numbers from 1 to 20 using while loop
num = 1
while num <= 20:
    if num % 2 == 0:
        print(num)
    num += 1 

#for loop- used to iterate over a sequence (like a list, tuple, string)
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    print(num)

