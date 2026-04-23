#1
class pepe:
    x = 5

obj = pepe()
print(obj.x)

#2 Class with multiple attributes
class phone:
    brand = "iphone"
    year = 2027

c = phone()
print(c.brand, c.year)

#3 Class with no attributes (empty blueprint)
class Empty:
    pass

e = Empty()
print(type(e))

#4 Class with attribute referencing another class
class Engine:
    power = "666 HP"

class Vehicle:
    engine = Engine()

v = Vehicle()
print(v.engine.power)

#5 Class with attribute that is a list
class PP2group:
    students = ["Qazbek", "Aruzhan", "Dias"]

sg = PP2group()
print(sg.students)