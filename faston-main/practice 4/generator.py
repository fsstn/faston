def squeres(n):
     for i in range(n+1):
          yield i**2

def evens(n):
     for i in range(n+1):
          if i % 2 == 0:
               yield f"{i}, "

def throur(n):
     for i in range(n+1):
          if i % 3 == 0 and i % 4 == 0:
               yield i

def AsqueresB(a, b):
     for i in range(a, b+1):
          yield i**2

def all(n):
     for i in range(n+1):
          yield i

#1
ans = squeres(int(input("Input number: ")))
for i in ans:
     print(i, end=" ")
print()

#2
ans = evens(int(input("Input number: ")))
for i in ans:
     print(i, end=" ")
print()

#3
ans = throur(int(input("Input number: ")))
for i in ans:
     print(i, end=" ")
print()

#4
ans = AsqueresB(int(input("Input first number: ")), int(input("Input second number: ")))
for i in ans:
     print(i, end=" ")
print()

#5
ans = all(int(input("Input number: ")))
for i in ans:
     print(i, end=" ")

