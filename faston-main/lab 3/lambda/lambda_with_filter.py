#1 Filter even numbers
nums = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)  

#2 Filter words longer than 5 letters
words = ["Bullet", "For", "My", "Valentine"]
long_words = list(filter(lambda w: len(w) > 5, words))
print(long_words)  

#3 Filter positive numbers
nums = [-3, -1, 0, 2, 5]
positives = list(filter(lambda x: x > 0, nums))
print(positives)  

#4 Filter names starting with 'B'
names = ["Dima", "Zheks", "Muha", "Miko"]
b_names = list(filter(lambda n: n.startswith("B"), names))
print(b_names)  

#5 Filter divisible by 3
nums = [3, 6, 7, 9, 10, 12]
div_by_three = list(filter(lambda x: x % 3 == 0, nums))
print(div_by_three)  