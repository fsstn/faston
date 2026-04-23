import os

# create folder
os.mkdir("test_folder")
print("Folder created")

# show list of files and folders
items = os.listdir(".")

print("List of items:")
for item in items:
    print(item)