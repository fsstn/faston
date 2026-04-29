#1 Stop when reaching 5
i = 1
while True:
    if i == 5:
        break
    print(i)
    i += 1

#2 Stop when user types "stop"
while True:
    word = input("Enter word: ")
    if word == "stop":
        break

#3 Find first even number
i = 1
while True:
    if i % 2 == 0:
        print("First even:", i)
        break
    i += 1

#4 Sum until reaching 100
s = 0
i = 1
while True:
    s += i
    if s >= 100:
        break
    i += 1
print("Sum =", s)

#5 Stop when negative number entered
while True:
    n = int(input("Enter number: "))
    if n < 0:
        break