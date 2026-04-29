#1 Sort by length of words
words = ["The", "World", "Is", "Yours"]
sorted_words = sorted(words, key=lambda w: len(w))
print(sorted_words) 

#2 Sort numbers by absolute value
nums = [-10, 5, -3, 2, -1]
sorted_abs = sorted(nums, key=lambda x: abs(x))
print(sorted_abs)  

#3 Sort tuples by second element
pairs = [(1, 3), (2, 1), (4, 2)]
sorted_pairs = sorted(pairs, key=lambda p: p[1])
print(sorted_pairs) 

#4 Sort names alphabetically by last letter
names = ["Bayern", "Vitality", "Ruchka", "Alim"]
sorted_names = sorted(names, key=lambda n: n[-1])
print(sorted_names)  

#5 Sort dictionary items by value
scores = {"Bayern": 90, "Vitality": 75, "Ruchka": 85}
sorted_scores = sorted(scores.items(), key=lambda item: item[1])
print(sorted_scores) 