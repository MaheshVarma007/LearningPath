from test import age, add_numbers, count
import pandas as pd


print(f"Count from test.py: {count}")
# Using the imported variable 'age' from test.py
print(f"Age from test.py: {age}")
# Using the imported function 'add_numbers' from test.py
result = add_numbers(10, 5)
print(f"Sum from test.py: {result}")