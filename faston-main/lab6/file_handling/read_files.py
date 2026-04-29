with open("sample.txt", "r") as f:
    # read() gets everything
    # readline() gets one line
    # readlines() returns a list of lines
    content = f.readlines()
    for line in content:
        print(f"Line: {line.strip()}")