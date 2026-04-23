
# list of names and scores
names = ["Ali", "Bob", "Tom"]
scores = [80, 90, 85]

# enumerate: show index and name
for i, name in enumerate(names):
    print("Index:", i, "Name:", name)

print()

# zip: combine two lists
for name, score in zip(names, scores):
    print(name, "-", score)

print()

# type checking
x = 10
y = "20"

print(type(x))  # int
print(type(y))  # str

# type conversion
y_int = int(y)
print("Converted y:", y_int)

# now we can add
print("Sum:", x + y_int)