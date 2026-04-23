#1 Shared class variable
class MyClass:
    x = 10

a = MyClass()
b = MyClass()
print(a.x, b.x)

#2 Changing class variable
class Counter:
    count = 0

Counter.count += 1
print(Counter.count)

#3 Class variable vs instance variable
class Person:
    species = "Human"

    def __init__(self, name):
        self.name = name

p = Person("Zheks")
print(p.name, p.species)

#4 Class variable used in method
class Circle:
    pi = 3.14

    def __init__(self, r):
        self.r = r

    def area(self):
        return Circle.pi * self.r * self.r

c = Circle(5)
print(c.area())

#5 Class variable as a list
class Group:
    members = []

Group.members.append("Qazz")
Group.members.append("Bolat")
print(Group.members)