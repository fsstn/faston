#1 using *args (variable number of positional arguments)
def sum_all(*args):
    return sum(args)

#2 using **kwargs (variable number of keyword arguments)
def describe_person(**kwargs):
    description = []
    for key, value in kwargs.items():
        description.append(f"{key}: {value}")
    return ", ".join(description)

#3 combining both *args and **kwargs
def demo_function(*args, **kwargs):
    return f"Args: {args}, Kwargs: {kwargs}"

# Example usage
print(sum_all(1, 2, 3, 4, 5))  
# Output: 15

# Example usage
print(demo_function(10, 20, x=5, y=15))  
# Output: Args: (10, 20), Kwargs: {'x': 5, 'y': 15}