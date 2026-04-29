# 1. Generator that generates squares up to N
def square_generator(N):
    for i in range(N + 1):   # go from 0 to N
        yield i * i          # return square

print("1) Squares up to 5:")
for num in square_generator(5):
    print(num, end=" ")
print("\n")


# 2. Generator to print even numbers 0..n comma separated
def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:       # check even number
            yield i

n = int(input("Enter n for even numbers: "))
print("2) Even numbers:")
print(",".join(str(x) for x in even_numbers(n)))
print()


# 3. Generator numbers divisible by 3 and 4
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

print("3) Numbers divisible by 3 and 4 up to 100:")
for num in divisible_by_3_and_4(100):
    print(num, end=" ")
print("\n")


# 4. Generator squares from a to b
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

print("4) Squares from 3 to 7:")
for num in squares(3, 7):
    print(num, end=" ")
print("\n")


# 5. Generator countdown from n to 0
def countdown(n):
    while n >= 0:
        yield n
        n -= 1

print("5) Countdown from 10:")
for num in countdown(10):
    print(num, end=" ")
print()