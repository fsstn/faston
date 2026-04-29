import os
from pathlib import Path

# Create nested directories
os.makedirs("parent/child/grandchild", exist_ok=True)

# List files and folders in current directory
print("Current Directory Contents:", os.listdir("."))

# Find files by extension (e.g., .py)
py_files = [f for f in os.listdir(".") if f.endswith(".py")]
print(f"Python files found: {py_files}")