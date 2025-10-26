from classes.person import Person
from classes.RollingWindow import RollingWindow

if __name__ == "__main__":
    # yusuf = Person("Yusuf Emir", 2003)
    # print(yusuf.name, yusuf.age)

    #print(type(RollingWindow.__dict__['capacity']).__name__)
    #

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