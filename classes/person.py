class Person:
    species = "Human"
    def __init__(self, name, birth_year):
        self.name = name
        self.birth_year = birth_year

    @property
    def age(self):
        from datetime import date
        current_year = date.today().year
        return current_year - self.birth_year