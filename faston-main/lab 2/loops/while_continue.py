#1 Skip even numbers
i = 1
while i <= 10:
    if i % 2 == 0:
        i += 1
        continue
    print(i)
    i += 1

#2 Skip empty input
i = 0
while i < 5:
    text = input("Enter text: ")
    i += 1
    if text == "":
        continue
    print("You entered:", text)

#3 Skip numbers less than 3
i = 0
while i < 6:
    i += 1
    if i < 3:
        continue
    print(i)

#4 Skip negative numbers
nums = [3, -1, 5, -2, 7]
i = 0
while i < len(nums):
    if nums[i] < 0:
        i += 1
        continue
    print(nums[i])
    i += 1

#5 Skip short words
words = ["cat", "house", "dog", "school"]
i = 0
while i < len(words):
    if len(words[i]) < 4:
        i += 1
        continue
    print(words[i])
    i += 1