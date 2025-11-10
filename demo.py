from classes.complex_number import ComplexNumber


if __name__ == "__main__":
    a = ComplexNumber(3, 4)
    b = ComplexNumber(1, -2)

    print(f"a: {a}")
    print(f"b: {b}")

    print(f"a + b: {a + b}")
    print(f"a - b: {a - b}")
    print(f"a * b: {a * b}")
    print(f"a / b: {a / b}")

    print(f"|a| (modulus of a): {a.magnitude}")
    print(f"arg(a) (argument of a): {a.argument}")
    print(f"conjugate of a: {a.conjugate()}")
    print(f"normalized a: {a.normalized()}")