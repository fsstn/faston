# Creating and writing to a file
with open("sample.txt", "w") as f:
    f.write("Hello Python!\n")
    f.write("This is Practice 6.\n")

# Appending new lines
with open("sample.txt", "a") as f:
    f.write("Appending a third line here.\n")