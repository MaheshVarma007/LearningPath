#Python

print("Hello, World!")

#name = input("Enter your name: ")
name2 = "Jack"
print(f"Hello, {name2}!")

#data types

# int
age = 30
print(f"Age: {age}")
# float
height = 5.9
print(f"Height: {height}")
# string
greeting = "Hello, World!"
print(greeting)
# boolean
is_student = True
print(f"Is student: {is_student}")
# list
fruits = ["apple", "banana", "cherry"]
print(f"Fruits: {fruits}")
# tuple
coordinates = (10.0, 20.0)
print(f"Coordinates: {coordinates}")
# dictionary
person = {"name": "Alice", "age": 25}
print(f"Person: {person}")
# set
unique_numbers = {1, 2, 3, 4, 5}
print(f"Unique numbers: {unique_numbers}")
# None
nothing = None
print(f"Nothing: {nothing}")


# Arithmetic operations
a = 10
b = 5
sum_result = a + b
print(f"Sum: {sum_result}")
difference_result = a - b
print(f"Difference: {difference_result}")
product_result = a * b
print(f"Product: {product_result}")
quotient_result = a / b
print(f"Quotient: {quotient_result}")
# Comparison operations
is_equal = (a == b)
print(f"Is equal: {is_equal}")
is_greater = (a > b)
print(f"Is greater: {is_greater}")
is_less = (a < b)
print(f"Is less: {is_less}")

# Logical operations
is_true = True

is_false = False
and_result = is_true and is_false
print(f"AND result: {and_result}")
or_result = is_true or is_false
print(f"OR result: {or_result}")
not_result = not is_true
print(f"NOT result: {not_result}")

age=70
# Conditional statements
if age < 18:
    print("You are a minor.")
elif age < 65:
    print("You are an adult.")
else:
    print("You are a senior citizen.") 

# Looping through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"Fruit: {fruit}")
# Looping through a range
for i in range(5):
    print(f"Number: {i}")
# While loop
count = 0
while count < 5:
    count= int(input("Enter a number (or type 5 to stop): "))
    print(f"Count: {count}")

# Function definition
def greet(name):
    print(f"Hello, {name}!")
    #return f"Hello, {name}!"


greet("Alice")
greet("Bob")
greet("Charlie")
# Function call
greeting_message = greet("Alice")
print(greeting_message)

# Function with return value
def add_numbers(a, b):
    return a + b   

result = add_numbers(10, 5)
print(f"Sum: {result}")

# Function with default parameter
def greet_with_default(name="Guest"):
    return f"Hello, {name}!"  

greeting_message = greet_with_default()
print(greeting_message)

# Function with variable number of arguments
def print_numbers(*args):
    for number in args:
        print(f"Number: {number}")

print_numbers(1, 2, 3, 4, 5)

# Function with keyword arguments
def print_person_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_person_info(name="Alice", age=25, city="New York")

# Lambda function
square = lambda x: x * x
print(f"Square of 5: {square(5)}")

# Map function
numbers = [1, 2, 3, 4, 5]
squared_numbers = list(map(lambda x: x * x, numbers))
print(f"Squared numbers: {squared_numbers}")

# Filter function
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Even numbers: {even_numbers}")

# Reduce function
from functools import reduce
sum_of_numbers = reduce(lambda x, y: x + y, numbers)
print(f"Sum of numbers: {sum_of_numbers}")

# List comprehensions
squared_numbers = [x * x for x in numbers]
print(f"Squared numbers using list comprehension: {squared_numbers}")

# Dictionary comprehensions
squared_dict = {x: x * x for x in numbers}
print(f"Squared numbers using dictionary comprehension: {squared_dict}")

# Set comprehensions
squared_set = {x * x for x in numbers}
print(f"Squared numbers using set comprehension: {squared_set}")

# Exception handling
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")    
except Exception as e:
    print(f"An unexpected error occurred: {e}")
# Finally block
finally:
    print("This block always executes.")

# File handling
try:
    with open("example.txt", "w") as file:
        file.write("Hello, World!")
    with open("example.txt", "r") as file:
        content = file.read()
        print(f"File content: {content}")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except IOError as e:
    print(f"IO error occurred: {e}")


    

