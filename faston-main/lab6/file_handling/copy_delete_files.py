import shutil
import os

# Copying a file
shutil.copy("sample.txt", "sample_backup.txt")

# Deleting the original file safely
if os.path.exists("sample.txt"):
    os.remove("sample.txt")
    print("Original file deleted.")