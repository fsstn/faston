from pathlib import Path
import shutil

# Create a source file and a destination folder
Path("data.txt").touch()
Path("archive").mkdir(exist_ok=True)

# Move the file
shutil.move("data.txt", "archive/data_v1.txt")