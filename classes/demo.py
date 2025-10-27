from classes.person import Person
from classes.RollingWindow import RollingWindow

from .RollingWindow import measure_time

@measure_time
def f1(x, y):
    return x + y


if __name__ == "__main__":
    # yusuf = Person("Yusuf Emir", 2003)
    # print(yusuf.name, yusuf.age)

    #print(type(RollingWindow.__dict__['capacity']).__name__)
    #
    #
    print(f1(10, 20))
    abc = RollingWindow(4)
    print(abc)
    abc.push(10)
    abc.push(20)
    abc.push(30)
    print(abc)
    print("Mean:", abc.mean)
    abc.push(40)
    print(abc)
    print("Mean:", abc.mean)
    abc.push(50)

    print(abc.values)


    abc.push(55)
    print(abc.values)