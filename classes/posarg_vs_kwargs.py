def somefunc(x: int, *, y: int) -> None:
    print(f"x: {x}, y: {y}")

if __name__ == "__main__":
    # correct way to call it
    somefunc(1, y=2)

    # incorrect way to call it
    # somefunc(1, 2)  # this will raise a TypeError