from functools import reduce

nums = [1, 2, 3, 4, 5, 6]

# map(): Square each number
squared = list(map(lambda x: x**2, nums))

# filter(): Keep only even numbers
evens = list(filter(lambda x: x % 2 == 0, nums))

# reduce(): Sum all numbers
total = reduce(lambda x, y: x + y, nums)

print(f"Squared: {squared}, Evens: {evens}, Total: {total}")