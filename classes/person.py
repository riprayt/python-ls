class Person:
    """a simple person class which will be extended later"""
    species = "Human"
    def __init__(self, name, birth_year):
        self.name = name
        self.birth_year = birth_year

    @property
    def age(self):
        """property decorator runs when you call person.age attribute"""
        from datetime import date
        current_year = date.today().year
        return current_year - self.birth_year