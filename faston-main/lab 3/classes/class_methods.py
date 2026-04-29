#1 Method printing a greeting
class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print("Hello, my name is " + self.name)

p = Person("Dima")
p.greet()

#2 Method returning a value
class Math:
    def square(self, x):
        return x * x

m = Math()
print(m.square(4))

#3 Method using multiple attributes
class Rectangle:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h

r = Rectangle(3, 4)
print(r.area())

#4 Method modifying an attribute
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

c = Counter()
c.increment()
print(c.count)

#5 Method with parameters
class Student:
    def __init__(self, name):
        self.name = name

    def introduce(self, subject):
        print(f"My name is {self.name}, I study {subject}.")

s = Student("Dima")
s.introduce("Python")