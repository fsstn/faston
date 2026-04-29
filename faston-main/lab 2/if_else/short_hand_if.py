#1 Short Hand If
a = 5
b = 2
if a > b: print("a is greater than b")

#2 Short Hand If-Else
a = 2
b = 330
print("A") if a > b else print("B")

#3 Short Hand If-Else with Variable Assignment
a = 10
b = 20
bigger = a if a > b else b
print("Bigger is", bigger)

#4 Multiple Conditions on One Line
a = 330
b = 330
print("A") if a > b else print("=") if a == b else print("B")

#5 example
x = 15
y = 20
max_value = x if x > y else y
print("Maximum value:", max_value)