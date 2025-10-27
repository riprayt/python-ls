def before(func):
    print("Before calling", func.__name__)
    return func

def after(func):
    print("After calling", func.__name__)
    return func

@after
@before
def some_function():
    print("Inside some_function")


if __name__ == "__main__":
    some_function()