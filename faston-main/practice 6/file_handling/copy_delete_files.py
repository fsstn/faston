import shutil
import os

# copy file
shutil.copy("example.txt", "copy.txt")
print("File copied")

# delete file (safe)
if os.path.exists("copy.txt"):
    os.remove("copy.txt")
    print("File deleted")
else:
    print("File not found")