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


def before_and_after(func):
    def wrapper(*args, **kwargs):
        print("Before calling", func.__name__)
        result = func(*args, **kwargs)
        print("After calling", func.__name__)
        return result
    return wrapper


@before_and_after
def another_function():
    print("Inside another_function")


if __name__ == "__main__":
    some_function()
    another_function()