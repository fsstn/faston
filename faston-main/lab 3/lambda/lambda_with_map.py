#1 Square numbers
nums = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, nums))
print(squares)  

#2 Convert to uppercase
words = ["Breaking", "Bad", "TheSopranos"]
upper_words = list(map(lambda w: w.upper(), words))
print(upper_words)  

#3 Add 10 to each number
nums = [5, 10, 15]
plus_ten = list(map(lambda x: x + 10, nums))
print(plus_ten)  

#4 Length of each word
words = ["Tony", "Soprano", "C#"]
lengths = list(map(lambda w: len(w), words))
print(lengths)  

#5 Double each element
nums = [2, 4, 6]
doubled = list(map(lambda x: x * 2, nums))
print(doubled)  