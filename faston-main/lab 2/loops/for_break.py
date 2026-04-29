#1 Stop when reaching 5
for i in range(1, 10):
    if i == 5:
        break
    print(i)

#2 Stop when finding "a"
for ch in "python":
    if ch == "a":
        break
    print(ch)

#3 Stop at negative number
nums = [3, 5, -1, 7]
for n in nums:
    if n < 0:
        break
    print(n)

#4 Find first even
for i in range(1, 10):
    if i % 2 == 0:
        print("First even:", i)
        break

#5 Stop at "stop"
for word in ["go", "run", "stop", "wait"]:
    if word == "stop":
        break
    print(word)