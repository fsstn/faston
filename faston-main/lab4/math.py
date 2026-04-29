import math

# 1. Convert degree to radian
degree = float(input("Input degree: "))
radian = degree * math.pi / 180
print("Output radian:", round(radian, 6))


# 2. Area of a trapezoid
h = float(input("\nHeight: "))
b1 = float(input("Base, first value: "))
b2 = float(input("Base, second value: "))
area_trap = (b1 + b2) * h / 2
print("Expected Output:", area_trap)


# 3. Area of regular polygon
n = int(input("\nInput number of sides: "))
s = float(input("Input the length of a side: "))
area_polygon = (n * s * s) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", int(area_polygon))


# 4. Area of a parallelogram
base = float(input("\nLength of base: "))
height = float(input("Height of parallelogram: "))
area_para = base * height
print("Expected Output:", float(area_para))