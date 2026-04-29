#1
def my_function(fname):
  print(fname + " Heisenberg")

my_function("Emily")
my_function("Tony")
my_function("Jackal")

#2
def my_function(name): # name is a parameter
  print("Hello", name)

my_function("Emily") # "Emily" is an argument

#3
def my_function(name = "friend"):
  print("Hello", name)

my_function("Emily")
my_function("Tony")
my_function("Jackal")

#4
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function(animal = "dog", name = "IshowSpeed")