def somefunc(x: int, *, y: int) -> None:
    print(f"x: {x}, y: {y}")

def f2(*args, **kwargs) -> None:

    print("args:", args, type(args))
    print("kwargs:", kwargs, type(kwargs))

    for i in args:
        print("arg:", i)
    for k, v in kwargs.items():
        print(f"kwarg: {k} = {v}")



if __name__ == "__main__":
    # correct way to call it
    somefunc(1, y=2)

    # incorrect way to call it
    # somefunc(1, 2)  # this will raise a TypeError

    f2(1, 2, a=3, b=4)
