#1 Count from 1 to 5
i = 1
while i <= 5:
    print(i)
    i += 1

#2 Sum numbers up to 10
i = 1
s = 0
while i <= 10:
    s += i
    i += 1
print("Sum =", s)

#3 Countdown
i = 5
while i > 0:
    print(i)
    i -= 1

#4 Read input until "exit"
text = ""
while text != "exit":
    text = input("Enter command: ")

#5 Print squares up to 10
i = 1
while i <= 10:
    print(i, i*i)
    i += 1