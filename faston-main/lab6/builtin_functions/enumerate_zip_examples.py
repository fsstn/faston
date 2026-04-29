names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

# enumerate(): Index and value
for index, name in enumerate(names):
    print(f"{index}: {name}")

# zip(): Pair two lists
for name, score in zip(names, scores):
    print(f"{name} scored {score}")