#1 return a single value
def square(x):
    return x * x

#2 return multiple values (as a tuple)
def divide(a, b):
    quotient = a // b
    remainder = a % b
    return quotient, remainder

#3 return a string
def format_name(first, last):
    return f"{last}, {first}"

#4 return a boolean
def is_even(n):
    return n % 2 == 0

#5 return a list
def multiples(n, count):
    return [n * i for i in range(1, count + 1)]