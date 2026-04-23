# write
with open("example.txt", "w") as file:
    file.write("Hello\n")

# append
with open("example.txt", "a") as file:
    file.write("New line\n")

# read
with open("example.txt", "r") as file:
    text = file.read()
    print(text)