
from functools import reduce

# list of numbers
numbers = [1, 2, 3, 4, 5]

# map: make square numbers
squares = list(map(lambda x: x * x, numbers))
print("Squares:", squares)

# filter: take only even numbers
even = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even)

# reduce: sum all numbers
total = reduce(lambda x, y: x + y, numbers)
print("Sum:", total)