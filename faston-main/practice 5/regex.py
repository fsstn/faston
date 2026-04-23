import re

# ---------------- 1 ----------------
# a затем 0 или больше b | a then zero or more b
text1 = "abbb"
pattern1 = r'ab*'
print("1:", bool(re.fullmatch(pattern1, text1)))

# ---------------- 2 ----------------
# a затем 2 или 3 b | a then two or three b
text2 = "abbb"
pattern2 = r'ab{2,3}'
print("2:", bool(re.fullmatch(pattern2, text2)))

# ---------------- 3 ----------------
# маленькие буквы соединенные _ | lowercase letters with underscore
text3 = "hello_world test_string example"
pattern3 = r'[a-z]+_[a-z]+'
print("3:", re.findall(pattern3, text3))

# ---------------- 4 ----------------
# одна большая буква затем маленькие | one uppercase then lowercase
text4 = "Hello World Python"
pattern4 = r'[A-Z][a-z]+'
print("4:", re.findall(pattern4, text4))

# ---------------- 5 ----------------
# строка начинается с a и заканчивается b | start with a end with b
text5 = "axxxb"
pattern5 = r'a.*b'
print("5:", bool(re.fullmatch(pattern5, text5)))

# ---------------- 6 ----------------
# заменить пробел , . на : | replace space comma dot with colon
text6 = "Hello, world. Python is fun"
result6 = re.sub(r'[ ,.]', ':', text6)
print("6:", result6)

# ---------------- 7 ----------------
# snake_case → camelCase
# перевод snake case в camel case
text7 = "hello_world_python"

words = text7.split("_")
camel = words[0] + ''.join(word.capitalize() for word in words[1:])
print("7:", camel)

# ---------------- 8 ----------------
# разделить строку по заглавным буквам | split at uppercase letters
text8 = "HelloWorldPython"
result8 = re.split(r'(?=[A-Z])', text8)
print("8:", result8)

# ---------------- 9 ----------------
# вставить пробелы перед заглавными буквами | insert space before capital
text9 = "HelloWorldPython"
result9 = re.sub(r'(?<!^)(?=[A-Z])', ' ', text9)
print("9:", result9)

# ---------------- 10 ----------------
# camelCase → snake_case
# перевод camel case в snake case
text10 = "helloWorldPython"

snake = re.sub(r'([A-Z])', r'_\1', text10).lower()
print("10:", snake)